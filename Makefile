img:
	docker build . -t ghcr.io/m3rone/busfs-server:latest

pubimg: img
	docker push ghcr.io/m3rone/busfs-server:latest
