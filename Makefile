push:
	rsync -auv /q/run/tenon/ qiuwch@xd:/q/run/tenon/

pull:
	rsync -auv qiuwch@xd:/q/run/tenon/ /q/run/tenon/

clean:
	rm -rf *.pyc __pycache__
