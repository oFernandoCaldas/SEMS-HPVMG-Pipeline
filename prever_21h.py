"""Gera as 24 previsões do dia seguinte com boletim disponível até a emissão."""
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib,pvlib
import sgie_pipeline as p

def predict_day(model,forecast,emission,c):
    emission=pd.Timestamp(emission)
    if emission.tzinfo is None:raise ValueError('Emissão deve incluir fuso, por exemplo 2026-09-03T21:00:00-03:00')
    emission=emission.tz_convert(c['timezone'])
    if emission.hour!=21 or emission.minute or emission.second:raise ValueError('Emissão esperada exatamente às 21h')
    f=forecast.copy();ix=p.index(f.pop('timestamp'),c)
    target_ix=pd.date_range(emission.normalize()+pd.Timedelta(days=1),periods=24,freq='h')
    expected_source=pd.date_range(target_ix[0],target_ix[-1]+pd.Timedelta(hours=1),freq='h')
    if not ix.is_unique or not ix.equals(expected_source):raise ValueError('Forneça 25 horários ordenados, de 00h do dia-alvo até 00h do dia seguinte; o último fornece GHI para o intervalo final')
    if 'issued_at' not in f:raise ValueError('Informe issued_at em cada linha do boletim arquivado')
    available=pd.DatetimeIndex(pd.to_datetime(f.issued_at))
    if available.tz is None:raise ValueError('issued_at deve incluir fuso')
    if available.isna().any() or (available>emission).any():raise ValueError('Boletim não disponível na emissão')
    if not set(c['features']).issubset(f.columns):raise ValueError('Boletim deve conter GHI, AirTemperature e WindSpeed')
    for col in c['features']:f[col]=pd.to_numeric(f[col],errors='raise')
    weather=f.set_axis(ix)
    x=weather.reindex(target_ix)[['AirTemperature','WindSpeed']].copy()
    x['GHI']=weather.GHI.reindex(target_ix+pd.Timedelta(hours=1)).to_numpy()
    x=x[c['features']]
    if not np.isfinite(x).all().all() or (x.GHI<0).any() or (x.WindSpeed<0).any():raise ValueError('Entradas meteorológicas alinhadas inválidas ou incompletas')
    source_available=pd.Series(available.to_numpy(),index=ix)
    ghi_available=source_available.reindex(target_ix+pd.Timedelta(hours=1))
    target_available=source_available.reindex(target_ix)
    zen_time=target_ix+pd.Timedelta(minutes=30)
    zen=pvlib.solarposition.get_solarposition(zen_time,latitude=c['latitude'],longitude=c['longitude'],altitude=c['altitude']).zenith.to_numpy()
    active=zen<=90
    result=pd.DataFrame({'timestamp':target_ix,'emissao':emission,'issued_at':target_available.to_numpy(),'issued_at_GHI':ghi_available.to_numpy(),'GHI_source_timestamp':target_ix+pd.Timedelta(hours=1),'zenite_timestamp':zen_time,'zenite_meio_intervalo':zen,'dentro_dominio_solar':active})
    result['previsao_modelo_kWh']=model.predict(x)
    # Intervalos parcialmente solares recebem extrapolação sinalizada, não validada pelo LOMO.
    # Zero somente quando o Sol permanece abaixo do horizonte em todo o intervalo [t,t+1h).
    zs=np.array([pvlib.solarposition.get_solarposition(target_ix+pd.Timedelta(minutes=int(m)),latitude=c['latitude'],longitude=c['longitude'],altitude=c['altitude']).zenith.to_numpy() for m in range(0,61,5)])
    fully_dark=(zs>90).all(axis=0)
    result['previsao_operacional_kWh']=result.previsao_modelo_kWh
    result.loc[fully_dark,'previsao_operacional_kWh']=0.
    result['status']=np.where(active,'modelo',np.where(fully_dark,'zero_regra_noturna','extrapolacao_intervalo_parcial_nao_validada'))
    result['horizonte_horas']=(target_ix-emission).total_seconds()/3600
    result['baseline_timestamp']=target_ix-pd.Timedelta(hours=24)
    result['baseline_timestamp_disponivel']=result.baseline_timestamp.le(emission)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--modelo',choices=['KRR','MLP','SVR','XGBoost'],required=True);ap.add_argument('--entrada',required=True);ap.add_argument('--emissao',required=True);ap.add_argument('--saida',required=True);ap.add_argument('--persistencia',help='CSV opcional timestamp,SystemProduction,available_at')
    args=ap.parse_args();c=p.read_config();r=p.BASE/'resultados'/c['run_id'];sig=json.loads((r/'assinatura.json').read_text())
    if sig!=p.signature():raise RuntimeError('Assinatura de dados/código/ambiente incompatível')
    model=joblib.load(r/'FINAL'/args.modelo/'modelo.joblib')
    out=predict_day(model,pd.read_csv(args.entrada),args.emissao,c)
    if args.persistencia:
        g=pd.read_csv(args.persistencia);g.index=p.index(g.pop('timestamp'),c)
        if not g.index.is_unique:raise ValueError('Persistência duplicada')
        if 'available_at' not in g:raise ValueError('Persistência operacional exige available_at com horário real de disponibilidade')
        av=pd.DatetimeIndex(pd.to_datetime(g.available_at))
        if av.tz is None:raise ValueError('available_at exige fuso')
        g['available_at']=av
        prev=g.reindex(pd.DatetimeIndex(out.baseline_timestamp));v=pd.to_numeric(prev.SystemProduction,errors='coerce').to_numpy();known=(prev.available_at<=pd.Timestamp(args.emissao)).to_numpy()
        good=np.isfinite(v)&(v>0)&out.baseline_timestamp_disponivel.to_numpy()&known
        out['persistencia_kWh']=np.where(good,v,np.nan);out['persistencia_valida']=good
    out.to_csv(args.saida,index=False)
    print(f'24 horários gravados em {args.saida}. Confira a coluna status; intervalos parcialmente solares são extrapolações identificadas, fora do domínio avaliado.')
if __name__=='__main__':main()
