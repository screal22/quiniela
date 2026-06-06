with partidos_con_resultados as (
	select p.nom_partido,
		   concat(r.resultado_1, ' - ', r.resultado_2) as resultado
	from partidos p
	left join resultados_partidos r
		on p.id = r.id_partido
	where r.resultado_1 >= 0
	order by p.id
	)
select *
from partidos_con_resultados;