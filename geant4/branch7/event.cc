#include "event.hh"
#include "G4AnalysisManager.hh"
#include "G4SDManager.hh"
#include "G4THitsMap.hh"
#include "G4SystemOfUnits.hh"

MyEventAction::MyEventAction() {}
MyEventAction::~MyEventAction() {}

void MyEventAction::BeginOfEventAction(const G4Event*) {}

void MyEventAction::EndOfEventAction(const G4Event* event)
{
    // 1. Acessa a tabela global de coleções do evento atual
    G4HCofThisEvent* hcofEvent = event->GetHCofThisEvent();
    if(!hcofEvent) return;

    // 2. Busca o ID da nossa coleção pelo nome direto
    G4SDManager* sdManager = G4SDManager::GetSDMpointer();
    G4int collectionID = sdManager->GetCollectionID("CristalCsI/Energia");
    if(collectionID < 0) return;

    // 3. Extrai o mapa de dados nativo
    G4THitsMap<G4double>* maptotal = (G4THitsMap<G4double>*)(hcofEvent->GetHC(collectionID));
    
    if(maptotal) {
        G4double energiaTotalDoEvento = 0.0;
        std::map<G4int, G4double*>* map = maptotal->GetMap();

        // Loop seguro para extrair os valores de double do mapa nativo do C++
        for(auto itr = map->begin(); itr != map->end(); itr++) {
            energiaTotalDoEvento += *(itr->second);
        }

        // Se o fóton depositou qualquer energia, por menor que seja, registra!
        if(energiaTotalDoEvento > 0.0) {
            auto analysisManager = G4AnalysisManager::Instance();
            analysisManager->FillH1(0, energiaTotalDoEvento, energiaTotalDoEvento);
            
            // Print de confirmação no terminal para você ver funcionando em tempo real:
            G4cout << "Energia depositada: " << energiaTotalDoEvento/MeV << " MeV" << G4endl;
        }
    }
}