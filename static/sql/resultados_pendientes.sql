select nom_partido
from partidos p
left join resultados_partidos r
	on p.id = r.id_partido
where cast(fecha_partido as date) <= current_date and resultado_1 is null;