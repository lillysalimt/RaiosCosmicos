#include "run.hh"
#include "G4AnalysisManager.hh"
#include "G4SystemOfUnits.hh"

MyRunAction::MyRunAction()
{
    auto analysisManager = G4AnalysisManager::Instance();
    analysisManager->SetDefaultFileType("csv");
    // Histograma ID = 0, 100 canais, de 5keV a 2.005*MeV
    analysisManager->CreateH1("PHS", "Espectro no CsI", 100, 5*keV, 2.005*MeV);
}

MyRunAction::~MyRunAction() {}

void MyRunAction::BeginOfRunAction(const G4Run*)
{
    auto analysisManager = G4AnalysisManager::Instance();
    analysisManager->OpenFile("Simulacao_100.csv"); // Força a extensão .csv
}

void MyRunAction::EndOfRunAction(const G4Run*)
{
    auto analysisManager = G4AnalysisManager::Instance();
    analysisManager->Write();
    analysisManager->CloseFile();
}