#include "construction.hh"

MyDetectorConstruction::MyDetectorConstruction()
{} 

MyDetectorConstruction::~MyDetectorConstruction()
{}

G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
    G4NistManager *nist = G4NistManager::Instance();

    // Ar
    G4Isotope* iso_N14  = new G4Isotope("N14",  7,  14, 14.00307*g/mole);
    G4Isotope* iso_O16  = new G4Isotope("O16",  8,  16, 15.99491*g/mole);
    G4Isotope* iso_Ar40 = new G4Isotope("Ar40", 18, 40, 39.96238*g/mole);
    G4Element* elN_puro  = new G4Element("Nitrogenio_Puro", "N",  1);
    elN_puro->AddIsotope(iso_N14, 100.0*perCent);
    G4Element* elO_puro  = new G4Element("Oxigenio_Puro",  "O",  1);
    elO_puro->AddIsotope(iso_O16, 100.0*perCent);
    G4Element* elAr_puro = new G4Element("Argonio_Puro",   "Ar", 1);
    elAr_puro->AddIsotope(iso_Ar40, 100.0*perCent);
    G4double densidadeAr = 0.001225 * g/cm3;
    G4int numComponentesM_Ar = 3;
    G4Material* m_Ar = new G4Material("Ar_Atmosferico", densidadeAr, numComponentesM_Ar, kStateGas);
    m_Ar->AddElement(elN_puro,  0.756); // 75.6% Nitrogênio-14
    m_Ar->AddElement(elO_puro,  0.231); // 23.1% Oxigênio-16
    m_Ar->AddElement(elAr_puro, 0.013); //  1.3% Argônio-40

    // Minério de ferro
    G4double densidadeMinerio = 3.5 * g/cm3;
    G4int numComponentesMinerio = 5;
    G4Material* m_Ore = new G4Material("Minerio_de_Ferro", densidadeMinerio, numComponentesMinerio);
    G4Element* elFe = nist->FindOrBuildElement("Fe");
    G4Element* elO  = nist->FindOrBuildElement("O");
    G4Element* elSi = nist->FindOrBuildElement("Si");
    G4Element* elAl = nist->FindOrBuildElement("Al");
    G4Element* elMn = nist->FindOrBuildElement("Mn");
    m_Ore->AddElement(elFe, 0.60); // 60% Ferro
    m_Ore->AddElement(elO,  0.30); // 30% Oxigênio
    m_Ore->AddElement(elSi, 0.05); //  5% Silício
    m_Ore->AddElement(elAl, 0.04); //  4% Alumínio
    m_Ore->AddElement(elMn, 0.01); //  1% Manganês

    // Chumbo
    G4Isotope* iso_Pb208 = new G4Isotope("Pb208", 82, 208, 207.9766*g/mole);
    G4Isotope* iso_Pb207 = new G4Isotope("Pb207", 82, 207, 206.9759*g/mole);
    G4Isotope* iso_Pb206 = new G4Isotope("Pb206", 82, 206, 205.9744*g/mole);
    G4Isotope* iso_Pb204 = new G4Isotope("Pb204", 82, 204, 203.9730*g/mole);
    G4Element* elPb_Isotopico = new G4Element("Chumbo_Isotopico", "Pb", 4);
    elPb_Isotopico->AddIsotope(iso_Pb208, 52.4*perCent);
    elPb_Isotopico->AddIsotope(iso_Pb207, 22.1*perCent);
    elPb_Isotopico->AddIsotope(iso_Pb206, 24.1*perCent);
    elPb_Isotopico->AddIsotope(iso_Pb204,  1.4*perCent);
    G4double densidadeChumbo = 11.34 * g/cm3;
    G4int numComponentesM_Pb = 1;
    G4Material* m_Pb = new G4Material("Chumbo", densidadeChumbo, numComponentesM_Pb);
    m_Pb->AddElement(elPb_Isotopico, 1.0);

    // Aço carbono
    G4Material* m_Aco = new G4Material("Aco", 7.85 * g/cm3, 2);
    G4Element* elC  = nist->FindOrBuildElement("C");
    m_Aco->AddElement(elFe, 0.98);
    m_Aco->AddElement(elC,  0.02);

    // CsI
    G4Element* elI  = nist->FindOrBuildElement("I");
    G4Element* elCs = nist->FindOrBuildElement("Cs");
    G4Material *detetorMat = new G4Material("Iodeto de Césio", 4.51*g/cm3, 2);
    detetorMat->AddElement(elI, 1);
    detetorMat->AddElement(elCs, 1);


    G4double energias_foton[] = {
        2.00*eV, 2.20*eV, 2.40*eV, 2.60*eV, 2.80*eV, 2.90*eV, 2.95*eV, // 2.95 eV é o seu pico (420 nm)
        3.00*eV, 3.10*eV, 3.20*eV, 3.40*eV, 3.60*eV, 3.80*eV, 4.00*eV
    };

    G4double rindexCsI[] = {1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8};
    G4double rindexAr[] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};

    G4double espectro_cintilacao[] = {
        0.01,    0.05,    0.15,    0.40,    0.75,    0.95,    1.00,
        0.95,    0.70,    0.45,    0.20,    0.08,    0.02,    0.00};

    G4double comprimento_absorcao[] = {
        1000.*mm, 1000.*mm, 1000.*mm, 1000.*mm, 900.*mm,  800.*mm,  750.*mm,
        700.*mm,  500.*mm,  300.*mm,  100.*mm,  10.*mm,   1.*mm,    0.1*mm};

    G4MaterialPropertiesTable *mptAr = new G4MaterialPropertiesTable();
    mptAr->AddProperty("RINDEX", energias_foton, rindexAr, 14);
    m_Ar->SetMaterialPropertiesTable(mptAr);

    G4MaterialPropertiesTable *mptCsI = new G4MaterialPropertiesTable();
    mptCsI->AddProperty("RINDEX", energias_foton, rindexCsI, 14);
    mptCsI->AddProperty("ABSLENGTH", energias_foton, comprimento_absorcao, 14);
    mptCsI->AddProperty("SCINTILLATIONCOMPONENT1", energias_foton, espectro_cintilacao, 14);

    mptCsI->AddConstProperty("SCINTILLATIONTIMECONSTANT1", 4.0*us);
    mptCsI->AddConstProperty("SCINTILLATIONYIELD", 43080./MeV);
    mptCsI->AddConstProperty("RESOLUTIONSCALE", 1.0);

    detetorMat->SetMaterialPropertiesTable(mptCsI);

    // Co60
    G4Isotope *Co59 = new G4Isotope("Co59", 27, 59, 58.9332*g/mole);
    G4Element *elCo = new G4Element("Cobalto", "Co", 1);
    elCo->AddIsotope(Co59, 100*perCent);
    G4Material* fonteMat = new G4Material("Co59", 8.9*g/cm3, 1);
    fonteMat->AddElement(elCo, 1);



    G4RotationMatrix* rotCylinder = new G4RotationMatrix();
    rotCylinder->rotateZ(90*deg);





    // Caixa de ar
    G4Box *solidMundo = new G4Box("solidMundo", 200*cm, 200*cm, 200*cm);
    G4LogicalVolume *logicMundo= new G4LogicalVolume(solidMundo, m_Ar, "logicMundo");
    G4VPhysicalVolume *physMundo = new G4PVPlacement(0, G4ThreeVector(0,0,0), logicMundo, "physMundo", 0, false, 0, true);

    // Fonte de Co
    G4Tubs* solidFonte = new G4Tubs("solidFonte", 0*cm, 0.35*cm, 30*cm, 0*deg, 360*deg);
    G4LogicalVolume* logicFonte = new G4LogicalVolume(solidFonte, fonteMat, "logicFonte");
    new G4PVPlacement(rotCylinder, G4ThreeVector(0, 0, 0), logicFonte, "physFonte", logicMundo, false, 0, true);

    // Esteira de alumínio
    G4Box *solidEsteira = new G4Box("solidEsteira", 25*cm, 0.5*mm, 75*cm);
    G4LogicalVolume *logicEsteira = new G4LogicalVolume(solidEsteira, m_Aco, "logicEsteira");
    new G4PVPlacement(0, G4ThreeVector(0,10.5*cm,0), logicEsteira, "physEsteira", logicMundo, false, 0, true);

    // Tarugo
    G4double meia_altura_tarugo = 7.8*cm;
    G4double centro_tarugo = (10.55*cm + meia_altura_tarugo);
    G4Box *solidTarugo = new G4Box("solidTarugo", 10*cm, meia_altura_tarugo, 10*cm);
    G4LogicalVolume *logicTarugo = new G4LogicalVolume(solidTarugo, m_Ore, "logicTarugo");
    new G4PVPlacement(0, G4ThreeVector(0, centro_tarugo, 0), logicTarugo, "physTarugo", logicMundo, false, 0, true);

    // Colimador de chumbo
    G4Tubs* solidColimadorBase = new G4Tubs("solidColimadorBase", 3.8*cm, 6.6*cm, 6.85*cm, 0*deg, 360*deg);
    G4Box* solidRecorte = new G4Box("solidRecorte", 3.8*cm, 3.0*cm, 3.8*cm);
    G4SubtractionSolid* solidColimadorFinal = new G4SubtractionSolid("solidColimadorFinal", solidColimadorBase, solidRecorte, 0, G4ThreeVector(4.8*cm, 0., 0.));
    G4LogicalVolume* logicColimador = new G4LogicalVolume(solidColimadorFinal, m_Pb, "logicColimador");
    new G4PVPlacement(rotCylinder, G4ThreeVector(0, 54.15*cm, 0), logicColimador, "physColimador", logicMundo, false, 0, true);

    // Disco de alumínio
    G4Tubs* solidDisco = new G4Tubs("solidDisco", 0*cm, 3.8*cm, 0.9*cm, 0*deg, 360*deg);
    G4LogicalVolume* logicDisco = new G4LogicalVolume(solidDisco, m_Aco, "logicDisco");
    new G4PVPlacement(rotCylinder, G4ThreeVector( 0, 54.15*cm, -3.4*cm), logicDisco, "physDisco", logicMundo, false, 0, true);

    // Clamping de alumínio
    G4Tubs* solidClamping = new G4Tubs("solidClamping", 0*cm, 3.8*cm, 14.55*cm, 0*deg, 360*deg);
    G4LogicalVolume* logicClamping = new G4LogicalVolume(solidClamping, m_Aco, "logicClamping");
    new G4PVPlacement(rotCylinder, G4ThreeVector(0, 54.15*cm, 17.05*cm), logicClamping, "physClamping", logicMundo, false, 0, true);


    // Detetor de CsI
    G4Tubs* solidDetetor = new G4Tubs("solidDetetor", 0*cm, 3.8*cm, 2.5*cm, 0*deg, 360*deg);
    logicDetetor = new G4LogicalVolume(solidDetetor, detetorMat, "logicDetetor");
    G4VPhysicalVolume* physDetetor = new G4PVPlacement(rotCylinder, G4ThreeVector(0, 54.15*cm, 0), logicDetetor, "physDetetor", logicMundo, false, 0, true);


    return physMundo;
}

void MyDetectorConstruction::ConstructSDandField()
{
    G4MultiFunctionalDetector* meuDetectorSensivel = new G4MultiFunctionalDetector("CristalCsI");
    G4SDManager::GetSDMpointer()->AddNewDetector(meuDetectorSensivel);

    G4VPrimitiveScorer* scorerEnergia = new G4PSEnergyDeposit("Energia");
    meuDetectorSensivel->RegisterPrimitive(scorerEnergia);

    // Garante a vinculação direta usando o ponteiro do volume lógico
    logicDetetor->SetSensitiveDetector(meuDetectorSensivel);
}




