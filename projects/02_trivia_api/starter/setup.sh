sudo -u postgres bash -c "psql -h 127.0.0.1 -p 5432 < /home/workspace/fsnd-/FSND/projects/02_trivia_api/starter/backend/setup.sql"
sudo -u postgres bash -c "psql -h 127.0.0.1 -p 5432 -d trivia < /home/workspace/fsnd-/FSND/projects/02_trivia_api/starter/backend/trivia.psql"
sudo -u postgres bash -c "psql -h 127.0.0.1 -p 5432 -d trivia_test < /home/workspace/fsnd-/FSND/projects/02_trivia_api/starter/backend/trivia.psql"
