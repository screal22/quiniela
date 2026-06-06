select nom_partido,
	   case
	   	when resultado_1 is null then '' 
		else concat(r.resultado_1, ' - ', r.resultado_2)
	   end as resultado
from partidos p
left join resultados_partidos r
	on p.id = r.id_partido
where cast(fecha_partido as date) = current_date;