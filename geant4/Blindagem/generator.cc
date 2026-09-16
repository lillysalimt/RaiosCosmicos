#include "generator.hh"


MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4ParticleGun(1);
}

MyPrimaryGenerator::~MyPrimaryGenerator()
{
    delete fParticleGun;
}

void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)

{
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4double tamanhoMundo = 50.0 * cm; 

        // ----------------------------------------------------
        // FONTE A: Cobalto-60
        // ----------------------------------------------------
        G4ParticleDefinition* particle = particleTable->FindParticle("gamma");
        fParticleGun->SetParticleDefinition(particle);
        G4double energiaCo60 = (G4UniformRand() < 0.5) ? 1.1732*MeV : 1.3325*MeV;
        fParticleGun->SetParticleEnergy(energiaCo60);

        G4double raioMax = 0.35 * cm;
        G4double metadeAltura = 30 * cm;
        G4double phi = G4UniformRand() * 360 * deg;
        G4double r = G4RandomRadiusInRing(0, raioMax);
        
        G4double xLocal = r * cos(phi);
        G4double yLocal = r * sin(phi);
        G4double zLocal = (G4UniformRand() * 2.0 - 1.0) * metadeAltura;

        G4ThreeVector posLocal(xLocal, yLocal, zLocal);

        G4RotationMatrix rotCylinder;
        rotCylinder.rotateZ(90 * deg);

        G4ThreeVector posMundo = rotCylinder * posLocal;

        fParticleGun->SetParticlePosition(posMundo);
        fParticleGun->SetParticleMomentumDirection(G4RandomDirection()); // Direcionado ao centro do detector

    // ========================================================
    fParticleGun->GeneratePrimaryVertex(anEvent);
}

