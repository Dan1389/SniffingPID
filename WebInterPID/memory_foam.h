#ifndef MEMORY_FOAM
#define MEMORY_FOAM

#include <EEPROM.h>

enum Flash_Error{
       MEM_OK=0,
       MEM_KO=1
};

class MemoryFoam
{
  public:
         Flash_Error write_memory(int address, uint8_t * data, int size);
         Flash_Error write_memory_wo_committ(int address, uint8_t * data, int size);
         Flash_Error committ();
         Flash_Error read_memory(int address, uint8_t * data, int size);
         Flash_Error clear_memory(int size);
         Flash_Error start_memory(int size);
         Flash_Error stop_memory();
};

#if !defined(NO_GLOBAL_INSTANCES) && !defined(NO_GLOBAL_EEPROM)
extern MemoryFoam MF;
#endif

#endif //MEMORY_FOAM
