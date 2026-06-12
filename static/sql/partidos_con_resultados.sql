with partidos_con_resultados as (
	select p.nom_partido,
		   case
			 	when r.resultado_1 is null then 'Sin resultado'
				else concat(r.resultado_1, ' - ', r.resultado_2)
			 end as resultado
	from postgres.public.partidos p
	left join postgres.public.resultados_partidos r
		on p.id = r.id_partido
	where fecha_partido < CURRENT_TIMESTAMP - INTERVAL '6 hours'
	order by p.id
	)
select *
from partidos_con_resultados;