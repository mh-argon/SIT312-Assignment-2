int led1 = D5;

void setup()
{

   pinMode(led1, OUTPUT);
   Particle.function("led",ledToggle);

   digitalWrite(led1, LOW);
}

void loop()
{

}

int ledToggle(String command) {

    if (command=="gateopen") {
        digitalWrite(led1,HIGH);
        return 1;
    }
    else if (command=="gateclose") {
        digitalWrite(led1,LOW);
        return 0;
    }
    else 
    {
        return -1;
    }
}
