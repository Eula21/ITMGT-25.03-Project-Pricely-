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
docker-compose up -d #starts the containers
docker ps -a # checks container status
docker stop pricely_search-web-1 pricely_search-celery-1 pricely_search-redis-1 # stops the containers

docker-compose restart web


docker pull redis:7







        const taglines = [
          "Shop smart. Live better.",
          "Where style meets savings.",
          "Everything you want. One cart away.",
          "Click. Cart. Celebrate.",
          "Better finds, better days.",
          "Your wallet loves Pricely.",
          "Pricely: where shopping gets smarter."
        ];

        let taglineIndex = 0;
        statusMessage.innerHTML = taglines[taglineIndex];
        statusMessage.classList.add("fade-in");

        const taglineInterval = setInterval(() => {
          statusMessage.classList.remove("fade-in");
          statusMessage.classList.add("fade-out");

          setTimeout(() => {
            taglineIndex = (taglineIndex + 1) % taglines.length;
            statusMessage.innerHTML = taglines[taglineIndex];
            statusMessage.classList.remove("fade-out");
            statusMessage.classList.add("fade-in");
          }, 500);
        }, 5000);
