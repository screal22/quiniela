select nom_partido
from postgres.public.partidos p
left join postgres.public.resultados_partidos r
	on p.id = r.id_partido
where cast(fecha_partido as date) <= current_date and resultado_1 is null;