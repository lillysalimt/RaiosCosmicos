#include "generator.hh"


static const std::vector<G4double> energias = {
    1.13E4*eV, 1.42E4*eV, 1.79E4*eV, 2.25E4*eV, 2.84E4*eV, 3.57E4*eV, 4.50E4*eV, 5.66E4*eV, 7.13E4*eV, 8.97E4*eV,
    1.13E5*eV, 1.42E5*eV, 1.79E5*eV, 2.25E5*eV, 2.84E5*eV, 3.57E5*eV, 4.50E5*eV, 5.66E5*eV, 7.13E5*eV, 8.97E5*eV,
    1.13E6*eV, 1.42E6*eV, 1.79E6*eV, 2.25E6*eV, 2.84E6*eV, 3.57E6*eV, 4.50E6*eV, 5.66E6*eV, 7.13E6*eV, 8.97E6*eV,
    1.13E7*eV, 1.42E7*eV, 1.79E7*eV, 2.25E7*eV, 2.84E7*eV, 3.57E7*eV, 4.50E7*eV, 5.66E7*eV, 7.13E7*eV, 8.97E7*eV,
    1.13E8*eV, 1.42E8*eV, 1.79E8*eV, 2.25E8*eV, 2.84E8*eV, 3.57E8*eV, 4.50E8*eV, 5.66E8*eV, 7.13E8*eV, 8.97E8*eV};

static const std::vector<G4double> fracoes_fotons = {
    4.75E-04, 1.40E-03, 4.10E-03, 1.20E-02, 3.44E-02, 9.03E-02, 1.76E-01, 2.03E-01, 1.57E-01, 1.06E-01,
    6.91E-02, 4.50E-02, 2.94E-02, 1.94E-02, 1.29E-02, 8.73E-03, 5.96E-03, 1.32E-02, 2.91E-03, 2.09E-03,
    1.52E-03, 1.12E-03, 8.41E-04, 6.39E-04, 4.90E-04, 3.79E-04, 2.95E-04, 2.30E-04, 1.79E-04, 1.38E-04,
    1.06E-04, 7.95E-05, 5.87E-05, 4.22E-05, 2.96E-05, 2.01E-05, 1.32E-05, 8.47E-06, 5.29E-06, 3.24E-06,
    1.95E-06, 1.16E-06, 6.83E-07, 3.99E-07, 2.32E-07, 1.35E-07, 7.77E-08, 4.48E-08, 2.58E-08, 1.49E-08};

static const std::vector<G4double> fracoes_muons_p = {3.110236220472441e-05, 3.818897637795276e-05, 4.68503937007874e-05, 5.767716535433071e-05, 
    7.086614173228347e-05, 8.700787401574803e-05, 0.00010708661417322835, 0.000131496062992126, 0.00016141732283464567, 0.00019881889763779528, 
    0.0002440944881889764, 0.00029921259842519685, 0.00036614173228346456, 0.00045078740157480316, 0.0005531496062992126, 0.0006771653543307086, 
    0.0008307086614173228, 0.0010157480314960628, 0.0012421259842519685, 0.0015177165354330708, 0.0018503937007874015, 0.002244094488188976, 
    0.0027362204724409446, 0.0033070866141732286, 0.0039960629921259845, 0.004803149606299213, 0.005748031496062992, 0.006850393700787402, 
    0.008110236220472442, 0.00952755905511811, 0.011141732283464567, 0.012952755905511811, 0.014960629921259842, 0.017204724409448816, 0.01968503937007874, 
    0.02263779527559055, 0.025984251968503937, 0.029921259842519685, 0.03405511811023622, 0.03858267716535433, 0.04291338582677165, 0.046456692913385826, 
    0.049606299212598425, 0.05177165354330709, 0.05295275590551181, 0.053149606299212594, 0.052362204724409445, 0.05059055118110236, 0.048031496062992125, 
    0.04468503937007874, 0.04094488188976378, 0.03661417322834645, 0.03208661417322834, 0.027362204724409447, 0.02263779527559055, 0.01811023622047244, 
    0.013976377952755905, 0.010374015748031496, 0.007401574803149606, 0.005059055118110236};

static const std::vector<G4double> fracoes_muons_n = {2.5925925925925925e-05, 3.224400871459695e-05, 4.008714596949891e-05, 4.967320261437908e-05, 
    6.187363834422658e-05, 7.66884531590414e-05, 9.52069716775599e-05, 0.00011830065359477123, 0.0001468409586056645, 0.00018235294117647057, 
    0.00022657952069716773, 0.0002810457516339869, 0.00034858387799564274, 0.0004313725490196078, 0.0005359477124183006, 0.0006644880174291938, 
    0.0008213507625272331, 0.0010174291938997821, 0.0012549019607843138, 0.0015490196078431374, 0.0019084967320261439, 0.002352941176470588, 
    0.002875816993464052, 0.003507625272331155, 0.004270152505446623, 0.005185185185185185, 0.006252723311546841, 0.00747276688453159, 0.00886710239651416, 
    0.010435729847494553, 0.012178649237472767, 0.014074074074074072, 0.0161437908496732, 0.018366013071895424, 0.020827886710239652, 0.023529411764705882, 
    0.02679738562091503, 0.030283224400871455, 0.03442265795206972, 0.038997821350762525, 0.04335511982570806, 0.047058823529411764, 0.05010893246187364, 
    0.05206971677559913, 0.05315904139433551, 0.05315904139433551, 0.05206971677559913, 0.04989106753812636, 0.047058823529411764, 0.04357298474945534, 
    0.03965141612200436, 0.03529411764705882, 0.03071895424836601, 0.025925925925925925, 0.021350762527233114, 0.01699346405228758, 0.013050108932461873, 
    0.009651416122004357, 0.006840958605664488, 0.004662309368191721};

G4double rInt = 90 * cm;
G4double rExt = 100.0 * cm;

G4double at_60Co = 7.4E4;
G4double at_concreto = 1.59E4;

// Atividade Expacs * 10^4 * 2pi // * 1.57
G4double at_fotons = 4.39E5; //1.09E5;
G4double at_muons_p = 2.482; // 0.62015; 
G4double at_muons_n = 2.274; // 0.56834;

G4double at_total = at_60Co + at_concreto + at_fotons + at_muons_p + at_muons_n;

G4double prob_60Co = at_60Co / at_total;
G4double prob_concreto = at_concreto / at_total;
G4double prob_fotons = at_fotons / at_total;
G4double prob_muons_p = at_muons_p / at_total;
G4double prob_muons_n = at_muons_n / at_total;

G4ThreeVector posDetector = G4ThreeVector(0, 54.15*cm, 0);

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
    G4double tamanhoMundo = 200.0 * cm; 

    G4double sorteioFonte = G4UniformRand();
    
    if (sorteioFonte < prob_60Co) 
    {
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
        fParticleGun->SetParticleMomentumDirection((posDetector - posMundo).unit()); // Direcionado ao centro do detector
    }
    else if (sorteioFonte < prob_60Co + prob_concreto)
    {
        // ----------------------------------------------------
        // FONTE B: RADIAÇÃO AMBIENTAL
        // ----------------------------------------------------
        G4ParticleDefinition* particle = particleTable->FindParticle("gamma");
        fParticleGun->SetParticleDefinition(particle);

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
        fParticleGun->SetParticleMomentumDirection((posDetector - posAmbiental).unit()); // Direcionado ao centro do detector
    }
    else if (sorteioFonte < prob_60Co + prob_concreto + prob_muons_p)
        {
        // ----------------------------------------------------
        // FONTE C: Muons+
        // ----------------------------------------------------
        G4ParticleDefinition* particle = particleTable->FindParticle("mu+");
        fParticleGun->SetParticleDefinition(particle);

        G4double rSorteio = G4UniformRand(); 
        G4double energiaSelecionada = energias[0]; // Valor padrão de segurança
        G4double somaAcumulada = 0.0;

        for (size_t i = 0; i < fracoes_muons_p.size(); ++i) {
            somaAcumulada += fracoes_muons_p[i];
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
        fParticleGun->SetParticleMomentumDirection((posDetector - posCosmica).unit()); // Direcionado ao centro do detector

    }

    else if (sorteioFonte < prob_60Co + prob_concreto + prob_muons_p + prob_muons_n)
        {
        // ----------------------------------------------------
        // FONTE D: Muons-
        // ----------------------------------------------------
        G4ParticleDefinition* particle = particleTable->FindParticle("mu-");
        fParticleGun->SetParticleDefinition(particle);

        G4double rSorteio = G4UniformRand(); 
        G4double energiaSelecionada = energias[0]; // Valor padrão de segurança
        G4double somaAcumulada = 0.0;

        for (size_t i = 0; i < fracoes_muons_n.size(); ++i) {
            somaAcumulada += fracoes_muons_n[i];
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
        fParticleGun->SetParticleMomentumDirection((posDetector - posCosmica).unit()); // Direcionado ao centro do detector

    }

    else
    {
        // ----------------------------------------------------
        // FONTE E: Fótons de raios cósmicos
        // ----------------------------------------------------
        G4ParticleDefinition* particle = particleTable->FindParticle("gamma");
        fParticleGun->SetParticleDefinition(particle);

        G4double rSorteio = G4UniformRand(); 
        G4double energiaSelecionada = energias[0]; // Valor padrão de segurança
        G4double somaAcumulada = 0.0;

        for (size_t i = 0; i < fracoes_fotons.size(); ++i) {
            somaAcumulada += fracoes_fotons[i];
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
        fParticleGun->SetParticleMomentumDirection((posDetector - posCosmica).unit()); // Direcionado ao centro do detector

    }

    // ========================================================
    fParticleGun->GeneratePrimaryVertex(anEvent);
}

