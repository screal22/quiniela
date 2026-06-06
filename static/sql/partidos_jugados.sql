select id, nom_partido
from postgres.public.partidos
where fecha_partido < CURRENT_TIMESTAMP - INTERVAL '6 hours'