void setup() {
  Serial.begin(9600);
}

void loop() {
  // Exemple : envoi d'angles aléatoires (remplace par tes capteurs)
  int angleX = random(0, 360);
  int angleY = random(0, 360);
  int angleZ = random(0, 360);

  // Envoi des angles sous la forme "X,Y,Z"
  Serial.print(angleX);
  Serial.print(",");
  Serial.print(angleY);
  Serial.print(",");
  Serial.println(angleZ);

  delay(1000); // Envoi toutes les secondes
}
