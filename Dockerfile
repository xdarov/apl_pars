FROM selenium/standalone-firefox:4.5.0-20221004

WORKDIR /home/seluser 
COPY . .
COPY autorun.sh /opt/bin/

RUN sudo apt-get update && \
	sudo apt-get upgrade --assume-yes && \
	sudo apt install --assume-yes python3.8-venv && \
	sudo apt-get install --assume-yes python3-pip && \
	sudo python3 -m venv venv && \
	sudo venv/bin/pip3 install --upgrade pip && \
	sudo venv/bin/pip3 install -r requirements.txt && \
	sudo chmod +x /opt/bin/autorun.sh
	
CMD ["/opt/bin/autorun.sh"]


