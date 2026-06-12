select nom_partido,
	   case
	   	when resultado_1 is null then '' 
		else concat(r.resultado_1, ' - ', r.resultado_2)
	   end as resultado
from postgres.public.partidos p
left join postgres.public.resultados_partidos r
	on p.id = r.id_partido
where cast(fecha_partido as date) = cast(CURRENT_TIMESTAMP - INTERVAL '6 hours' as date);