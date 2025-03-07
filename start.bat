kubectl apply -f backuppv.yaml 
kubectl get pv backup-pv
kubectl apply -f backuppvc.yaml 
kubectl get pvc backup-pvc
kubectl apply -f cronjob.yaml 
kubectl get cronjob backup-cronjob 