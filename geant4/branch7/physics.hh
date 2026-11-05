#ifndef PHYSICS_HH
#define PHYSICS_HH

#include "G4VModularPhysicsList.hh"
#include "G4EmStandardPhysics.hh"
#include "G4OpticalPhysics.hh"


#include "FTFP_BERT.hh" // Herdando diretamente da lista oficial

class MyPhysicsList : public FTFP_BERT
{
public:
    MyPhysicsList();
    virtual ~MyPhysicsList() override;

    // Sobrescrevemos o método que define os cortes
    virtual void SetCuts() override;
};

#endif