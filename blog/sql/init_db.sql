create database aiohttp_social_network;
CREATE USER simpleuser WITH PASSWORD 'myVeryLongPassword';
ALTER DATABASE aiohttp_social_network OWNER TO simpleuser;
GRANT ALL PRIVILEGES ON DATABASE aiohttp_social_network TO simpleuser;
grant usage on schema public to simpleuser
