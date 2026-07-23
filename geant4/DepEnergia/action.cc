#include "action.hh"

MyActionInitialization::MyActionInitialization()
{}

MyActionInitialization::~MyActionInitialization()
{}

void MyActionInitialization::BuildForMaster() const
{
    SetUserAction(new MyRunAction());

}

void MyActionInitialization::Build() const
{
    SetUserAction(new MyPrimaryGenerator());
    SetUserAction(new MyRunAction());
    SetUserAction(new MyEventAction());

}