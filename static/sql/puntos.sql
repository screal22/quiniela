with puntos as (
	select p.nom_partido,
		   p.fecha_partido,
		   r.resultado_1,
		   r.resultado_2,
		   pr.pronostico_1,
		   pr.pronostico_2,
		   pr.added_date at TIME zone 'America/Mexico_City' as alta_pronostico,
		   pr.participante
	from partidos p
	left join resultados_partidos r
		on p.id = r.id_partido
	left join pronosticos pr
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
			   or (resultado_2 > resultado_1 and pronostico_2 > pronostico_1) then 1
			else 0   
		   end as total_puntos
	from puntos
	),
puntos_3 as (
	select participante,
		   sum(case
		   	when total_puntos = 3 then 1
			else 0
		   end) as total_aciertos,
		   sum(total_puntos) as total_puntos
	from puntos_2
	group by participante
	)
select *
from puntos_3;