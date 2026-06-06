with partidos_con_resultados as (
	select p.nom_partido,
		   concat(r.resultado_1, ' - ', r.resultado_2) as resultado
	from postgres.public.partidos p
	left join postgres.public.resultados_partidos r
		on p.id = r.id_partido
	where r.resultado_1 >= 0
	order by p.id
	)
select *
from partidos_con_resultados;