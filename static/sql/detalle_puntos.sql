with puntos as (
	select p.nom_partido,
		   p.fecha_partido,
		   r.resultado_1,
		   r.resultado_2,
		   pr.pronostico_1,
		   pr.pronostico_2,
		   pr.added_date - INTERVAL '6 hours' as alta_pronostico,
		   pr.participante
	from postgres.public.partidos p
	left join postgres.public.resultados_partidos r
		on p.id = r.id_partido
	left join postgres.public.pronosticos pr
		on p.id = pr.id_partido
	where r.resultado_1 >= 0
	),
puntos_2 as (
	select *,
		   case
		   	when (fecha_partido >= alta_pronostico) = False then 0
		   	when (pronostico_1 = -1) or (pronostico_2 = -1) then 0
		   	when resultado_1 = pronostico_1 and resultado_2 = pronostico_2 then 3
		   	when (resultado_1 > resultado_2 and pronostico_1 > pronostico_2)
			   or (resultado_2 > resultado_1 and pronostico_2 > pronostico_1)
			   or (resultado_1 = resultado_2 and pronostico_1 = pronostico_2) then 1
			else 0   
		   end as total_puntos
	from puntos
	)
select *
from puntos_2;