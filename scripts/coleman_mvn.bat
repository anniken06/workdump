cd "C:\Users\jguzman2\git\coleman.ui"

(cd com.infor.colemanui.ui && mvn clean install && cd ..\com.infor.colemanui.backend && mvn clean install -DskipTests && cd ..\com.infor.colemanui.spring.backend && mvn clean install && cd ..\com.infor.colemanui.execution.emr && mvn clean install && echo "Finished building with no errors." && PAUSE) || PAUSE