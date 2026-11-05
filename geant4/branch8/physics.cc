#include "physics.hh"
#include "G4OpticalPhysics.hh"

MyPhysicsList::MyPhysicsList() : FTFP_BERT() // Inicializa a base FTFP_BERT primeiro
{
    // A FTFP_BERT já vem com TODA a física EM e Hadrônica.
    RegisterPhysics(new G4OpticalPhysics());
}

MyPhysicsList::~MyPhysicsList()
{}

void MyPhysicsList::SetCuts()
{
    // Executa os cortes padrão da FTFP_BERT
    FTFP_BERT::SetCuts();
}