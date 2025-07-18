Message:
    we're using redis to store temporary information such as the recent scraped data from users' search, it's faster to do this with redis
    we're using SQLite to store permanent data such as user authentication data
    we're using docker to run redis 'cause apparently, it's better that way compared to running emulators to download redis pa and we're already gonna use docker anyways naman

    lowkey, we should remove the space between pricely and the version for our folder names, quite a hassle moving through directories hehe

    for the info we will provide, the store store inside the e-commerce website is hard to get, like for Lazada and Amazon, they don't show it unless you click on the link
    I can automate this but it will make the information retrieval slower, what do we think about this?

Note:
    ### Make sure na venv is always activated.

    docker rm -f redis
        this code removes redis from docker
    docker run -d -p 6379:6379 --name redis redis 
        this code was used to create a new container, you only need to run this once 
    docker start redis
        use this code to use redis through docker in next iterations
    docker ps 
        use this code if you wanna make sure that redis is running, redis must be in the list, under the Image column I think

    # dudes, Idunno why this is happening but better to do this nalang: delete and then create redis in the container again
    # I think nothing bad is gonna happen if we do that 'cause we're using redis naman to like run tasks and store temporary data

    celery -A pricely_search worker --loglevel=info
        use this to run celery, fair warning, open a new terminal once this is a success hehe
        celery -A pricely_search worker --loglevel=info --pool=solo
            use this for Windows, this is to run an isolated inst
    
    how to test if celery is working:
    python manage.py shell ## do this in a different terminal from the one on top or just run the server
        run this:
            from core.tasks import run_amazon_scraper
            result = run_amazon_scraper.delay("mcdonalds")
        when you run that, you should be able to see something like this: [2025-07-16 01:23:48,147: INFO/MainProcess] Task core.tasks.run_amazon_scraper[d8e9a366-5e80-4f6c-ab97-5748b4615007] received
        this means that celery received the task
        then an output will be given like with the product name na, this means that the task has been executed mwehehe hurrah!

    pip freeze > requirements.txt
        update requirements.txt using this code after you add new dependencies or libraries

New files:
    celery.py
    tasks.py
    WF_Lazada.py
    WF_SM.py
    WF_Uniqlo.py
    WF_eBay.py
    Dockerfile
    docker_compose.yml

    Lyss integration: static folder and the stuff inside it
    
Edited files:
    settings.py (lines 124 to 127)
    pricely_search/__init__.py (lines 1 to 3)

What I want to do:
    Imma prolly add H&M, Gap, etc. if we have more time
    my working assumption is that since they are in the first page, they would either come from reputable stores or extremely marketed which means the store is quite established due to how much they are willing to pay for marketing

What I want to see:
    A funny loading thingy so that users won't get bored.
    Please do mapping nalang to change the currency.

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
