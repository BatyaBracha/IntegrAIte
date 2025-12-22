FROM jenkins/jenkins:lts

USER root

# העתקת התעודה שנמצאת איתך באותה תיקייה
COPY netfree-ca-bundle-curl.crt /usr/local/share/ca-certificates/netfree.crt

# עדכון מאגר התעודות של מערכת ההפעלה
RUN update-ca-certificates

# הוספת התעודה ל-TrustStore של Java שבו ג'נקינס משתמש
RUN keytool -import -alias netfree -keystore $JAVA_HOME/lib/security/cacerts \
    -file /usr/local/share/ca-certificates/netfree.crt -storepass changeit -noprompt

USER jenkins