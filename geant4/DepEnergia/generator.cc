#include "generator.hh"


static const std::vector<G4double> energias = {
    1.13E4*eV, 1.42E4*eV, 1.79E4*eV, 2.25E4*eV, 2.84E4*eV, 3.57E4*eV, 4.50E4*eV, 5.66E4*eV, 7.13E4*eV, 8.97E4*eV,
    1.13E5*eV, 1.42E5*eV, 1.79E5*eV, 2.25E5*eV, 2.84E5*eV, 3.57E5*eV, 4.50E5*eV, 5.66E5*eV, 7.13E5*eV, 8.97E5*eV,
    1.13E6*eV, 1.42E6*eV, 1.79E6*eV, 2.25E6*eV, 2.84E6*eV, 3.57E6*eV, 4.50E6*eV, 5.66E6*eV, 7.13E6*eV, 8.97E6*eV,
    1.13E7*eV, 1.42E7*eV, 1.79E7*eV, 2.25E7*eV, 2.84E7*eV, 3.57E7*eV, 4.50E7*eV, 5.66E7*eV, 7.13E7*eV, 8.97E7*eV,
    1.13E8*eV, 1.42E8*eV, 1.79E8*eV, 2.25E8*eV, 2.84E8*eV, 3.57E8*eV, 4.50E8*eV, 5.66E8*eV, 7.13E8*eV, 8.97E8*eV
};

static const std::vector<G4double> fracoes = {
    4.75E-04, 1.40E-03, 4.10E-03, 1.20E-02, 3.44E-02, 9.03E-02, 1.76E-01, 2.03E-01, 1.57E-01, 1.06E-01,
    6.91E-02, 4.50E-02, 2.94E-02, 1.94E-02, 1.29E-02, 8.73E-03, 5.96E-03, 1.32E-02, 2.91E-03, 2.09E-03,
    1.52E-03, 1.12E-03, 8.41E-04, 6.39E-04, 4.90E-04, 3.79E-04, 2.95E-04, 2.30E-04, 1.79E-04, 1.38E-04,
    1.06E-04, 7.95E-05, 5.87E-05, 4.22E-05, 2.96E-05, 2.01E-05, 1.32E-05, 8.47E-06, 5.29E-06, 3.24E-06,
    1.95E-06, 1.16E-06, 6.83E-07, 3.99E-07, 2.32E-07, 1.35E-07, 7.77E-08, 4.48E-08, 2.58E-08, 1.49E-08
};

G4double rInt = 90.0 * cm;
G4double rExt = 100.0 * cm;

G4double at_60Co = 7.4E4;
G4double at_concreto = 1.59E4;
G4double at_cosmicos = 4.39E5;
G4double at_total = at_60Co + at_concreto + at_cosmicos;

G4double prob_60Co = at_60Co / at_total;
G4double prob_concreto = at_concreto / at_total;
G4double prob_cosmicos = at_cosmicos / at_total;

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
    G4ParticleDefinition* particle = particleTable->FindParticle("gamma");
    fParticleGun->SetParticleDefinition(particle);
    G4double tamanhoMundo = 200.0 * cm; 

    G4double sorteioFonte = G4UniformRand();
    
    if (sorteioFonte < prob_60Co) 
    {
        // ----------------------------------------------------
        // FONTE A: Cobalto-60
        // ----------------------------------------------------
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
        fParticleGun->SetParticleMomentumDirection(G4RandomDirection()); // Isotrópico
    }
    else if (sorteioFonte < prob_60Co + prob_concreto)
    {
        // ----------------------------------------------------
        // FONTE B: RADIAÇÃO AMBIENTAL
        // ----------------------------------------------------
        fParticleGun->SetParticleEnergy(1.46 * MeV);

        G4double rCubeAmbient = G4Pow::GetInstance()->powA(rInt, 3) + 
                                G4UniformRand() * (G4Pow::GetInstance()->powA(rExt, 3) - G4Pow::GetInstance()->powA(rInt, 3));
        G4double rSorteadoAmbient = G4Pow::GetInstance()->powA(rCubeAmbient, 1.0/3.0);

        G4ThreeVector direcaoAleatoriaAmbient = G4RandomDirection();

        if (direcaoAleatoriaAmbient.y() > 0) {
            direcaoAleatoriaAmbient.setY(-direcaoAleatoriaAmbient.y());
        }

        G4ThreeVector posAmbiental = direcaoAleatoriaAmbient * rSorteadoAmbient;
        fParticleGun->SetParticlePosition(posAmbiental);
        fParticleGun->SetParticleMomentumDirection(G4RandomDirection()); // Isotrópico
    }
    else
    {
        // ----------------------------------------------------
        // FONTE C: RAIOS CÓSMICOS
        // ----------------------------------------------------

        G4double rSorteio = G4UniformRand(); 
        G4double energiaSelecionada = energias[0];
        G4double somaAcumulada = 0.0;

        for (size_t i = 0; i < fracoes.size(); ++i) {
            somaAcumulada += fracoes[i];
            if (rSorteio <= somaAcumulada) {
                energiaSelecionada = energias[i];
                break;
            }
        }
        fParticleGun->SetParticleEnergy(energiaSelecionada);

        G4double rCube = G4Pow::GetInstance()->powA(rInt, 3) + 
                 G4UniformRand() * (G4Pow::GetInstance()->powA(rExt, 3) - G4Pow::GetInstance()->powA(rInt, 3));
        G4double rSorteado = G4Pow::GetInstance()->powA(rCube, 1.0/3.0);

        G4ThreeVector direcaoAleatoria = G4RandomDirection();

        if (direcaoAleatoria.y() < 0) {
        direcaoAleatoria.setY(-direcaoAleatoria.y());
        }
        G4ThreeVector posCosmica = direcaoAleatoria * rSorteado;

        fParticleGun->SetParticlePosition(posCosmica);
        fParticleGun->SetParticleMomentumDirection(G4RandomDirection()); // Isotrópico

    }

    // ========================================================
    fParticleGun->GeneratePrimaryVertex(anEvent);
}

