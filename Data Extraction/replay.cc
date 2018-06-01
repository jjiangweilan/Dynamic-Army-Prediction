#include "sc2api/sc2_api.h"

#include "sc2utils/sc2_manage_process.h"

#include <string>

#include <iostream>

#include <vector>

#include <fstream>

#include <sstream>

#include <iostream>

//The Replay texts get sent to the s2client-api\build\bin folder
//json won't work?
//https://github.com/nlohmann/json
#include "C:/Users/jjian_000/Desktop/Replays" // the json hpp

//put your replay folder here
const char* kReplayFolder = "";

class Replay : public sc2::ReplayObserver {
public:
    std::vector<uint32_t> count_units_built_;
    std::set<uint64_t> unitsc;
    int inte = 1;
    std::string UnitLog;
    std::map<std::string, std::vector<int>> arrayTime;
    
    Replay() :
    sc2::ReplayObserver() {
    }
    
    void OnGameStart() final {
        const sc2::ObservationInterface* obs = Observation();
        assert(obs->GetUnitTypeData().size() > 0);
        count_units_built_.resize(obs->GetUnitTypeData().size());
        std::fill(count_units_built_.begin(), count_units_built_.end(), 0);
        std::string RepNum;
        std::ostringstream con;
        con << inte;
        RepNum = con.str();
        //Initialize Text file for Unit Composition
        UnitLog = "Replay " + RepNum + "UnitLog.txt";
        //Initialize Text log for json not done
        std::ofstream myfile (UnitLog);
        //clear map
        arrayTime.clear();
        }
        
        void OnUnitCreated(const sc2::Unit* unit) final {
            assert(uint32_t(unit->unit_type) < count_units_built_.size());
            //increment only if its a new unit tag
            std::set<uint64_t>::iterator iter = unitsc.find(unit->tag);
            //map of unit name and time
            //stores the unit types into the log
            std::ofstream myfile;
            myfile.open (UnitLog, std::ios::app);
            
            if (iter != unitsc.end()) {
                //std::cout << "Existing Unit Found" << std::endl;
            }
            else {
                //json won't work
                //nlohmann::json jsonForm[unit->unit_type] = Observation()->GetGameLoop();
                unitsc.insert(unit->tag);
                //insert into make as a unit/time pairing
                arrayTime[sc2::UnitTypeToName(unit->unit_type)];
                arrayTime[sc2::UnitTypeToName(unit->unit_type)].push_back(Observation()->GetGameLoop());
                //std::cout << arrayTime.size() << "this is it" << std::endl;
                ++count_units_built_[unit->unit_type];
                //std::cout << "New Unit Found!" << std::endl;
                //myfile << "A " <<  sc2::UnitTypeToName(unit->unit_type) << " was created on " << Observation()->GetGameLoop() << "\n";
            }
        }
        
        void OnStep() final {
        }
        
        void OnGameEnd() final {
            //std::cout << "Units created:" << std::endl;
//            const sc2::ObservationInterface* obs = Observation();
//            const sc2::UnitTypes& unit_types = obs->GetUnitTypeData();
//            for (uint32_t i = 0; i < count_units_built_.size(); ++i) {
//                if (count_units_built_[i] == 0) {
//                    continue;
//                }
//
//                std::cout << unit_types[i].name << ": " << std::to_string(count_units_built_[i]) << std::endl;
//            }
            //https://stackoverflow.com/questions/1063453/how-to-display-map-contents
            //Displays map contents
//            for(auto it = arrayTime.cbegin(); it != arrayTime.cend(); ++it)
//            {
//                std::cout << it->first << " : ";
//                for(auto it2 = it->second.begin(); it2 != it->second.end(); ++it2){
//                    if (it2 != it->second.end()) {
//                        printf("%i, ", *it2);
//                    }
//                    else {
//                        printf("%i\n", *it2);
//                    }
//                }
//            }
            
            nlohmann::json jj(arrayTime);
            auto f = std::ofstream();
            f.open("data.json", std::ios_base::app);
            f << jj.dump();
            f << "," << std::endl;
            f.close();
            std::cout << jj.dump();
            std::cout << "Finished" << std::endl;
            std::cout << "This was Replay " << inte;
            inte++;
        }
};
        
int main(int argc, char* argv[]) {
    sc2::Coordinator coordinator;
    if (!coordinator.LoadSettings(argc, argv)) {
        return 1;
    }
    
    if (!coordinator.SetReplayPath(kReplayFolder)) {
        std::cout << "Unable to find replays." << std::endl;
        return 1;
    }
    
    
    Replay replay_observer;
    
    coordinator.AddReplayObserver(&replay_observer);
    
    while (coordinator.Update());
    while (!sc2::PollKeyPress());
}
