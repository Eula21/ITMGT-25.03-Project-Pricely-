Message:

Note:

New files:

    
Edited files:


What I want to do:

What I want to see:

Notes to self:
    WF_Amazon.py, scrape_amazon(query)
    WF_Lazada.py, scrape_lazada(query)
    WF_SM.py, scrape_SM(query)
    WF_Uniqlo.py, scrape_uniqlo(query)
    WF_eBay.py, scrape_ebay(query)

! Don't use docker muna. Made me cry, but will integrate better after frontend.
Steps on how to set up your environment:
    hiii, bare with me, this can be a lot
        1.)  ## download venv using requirements.txt
        2.) docker build -t pricely .
        3.) docker-compose up --build ## runs both django and celery ## reco this
                docker run -p 8000:8000 pricely ## run the website through docker but without celery|redis
                ** once running, access the website through: http://localhost:8000/


docker rm -f redis
docker run -d -p 6379:6379 --name redis redis
docker start redis
docker ps


pip install -r pricely_search\requirements.txt 
pip freeze

celery -A pricely_search worker --loglevel=info --pool=solo

docker build -t pricely_web .
docker-compose build

docker system prune -af
docker-compose build
docker-compose up

to update:
docker-compose build
docker-compose up -d

docker pull redis:7