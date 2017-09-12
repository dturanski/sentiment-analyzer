# Sentiment Analyzer

A tweet sentiment analyzer using ML based on https://github.com/crawles/text-analytics-service-example . This [implementation](../blob/master/app/sentiment-service.py) uses the [springcloudstream](https://github.com/dturanski/springcloudstream) 
framework to bind the given function to a TCP server for easy integration with something like the Spring Cloud Stream [tcp client processor](https://github.com/spring-cloud-stream-app-starters/tcp/tree/master/spring-cloud-starter-stream-processor-tcp-client).


# Running Standalone

## Show the usage message
````bash
$ python app/sentiment-service.py --help
Usage: sentiment-service.py [options] --help for help

Options:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  the socket port to use
  -m MONITOR_PORT, --monitor-port=MONITOR_PORT
                        the socket to use for the monitoring server
  -s BUFFER_SIZE, --buffer-size=BUFFER_SIZE
                        the tcp buffer size
  -d, --debug           turn on debug logging
  -c CHAR_ENCODING, --char-encoding=CHAR_ENCODING
                        character encoding
  -e ENCODER, --encoder=ENCODER
                        The name of the encoder to use for delimiting messages
 ````                       

## Start the server
````bash
$ python app/sentiment-service.py --port 9999 --monitor-port 9998 --debug

````

## Use `netcat` to talk to it. 



````bash
$nc localhost 9999
````
The expected input is a list of raw tweets as json. The only required field is `text`. So the simplest input message is something like.
````json
[{"text":"this is really FANTASTIC!!!!"}]
[{"polarity": 0.7, "text": "this is really FANTASTIC!!!!"}]
````
The output is a list of items containing the original text and a score called `polarity`, a number between 0 and 1 where a higher value indicates a positive sentiment.

````json
[{"text":"it's wonderful to be in love. Life is great!"}, {"text":"This has to be the worst food I've ever eaten"},{"text":"I had pizza for dinner"}]
[{"polarity": 0.97, "text": "it's wonderful to be in love. Life is great!"}, {"polarity": 0.06, "text": "This has to be the worst food I've ever eaten"}, {"polarity": 0.64, "text": "I had pizza for dinner"}]
````

# Building and Running the Docker image
The `Dockerfile` provided starts with an [Miniconda](https://conda.io/miniconda.html) image and creates a virtual environment specified in [app/environment.yml](../master/blob/app/environment.yml).

````bash
$ docker build . -t dturanski/sentiment-analyzer:latest
$ docker run -p9999:9999 -p9998:9998 -it dturanski/sentiment-analyzer:latest 
````
