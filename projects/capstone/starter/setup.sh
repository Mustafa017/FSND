sudo -u postgres bash -c "psql -h 127.0.0.1 -p 5432 < /home/projects/web/FSND/projects/capstone/starter/backend/setup.sql"
sudo -U postgres bash -c "psql -h 127.0.0.1 -p 5432 -d school_management < /home/projects/web/FSND/projects/capstone/starter/backend/database.psql"
sudo -u postgres bash -c "psql -h 127.0.0.1 -p 5432 -d school_management_test < /home/projects/web/FSND/projects/capstone/starter/backend/database.psql"
