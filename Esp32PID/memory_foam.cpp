#include "memory_foam.h"

Flash_Error MemoryFoam::write_memory(int address, uint8_t * data, int size){
	
	int i=0;
	
	for (i=0;i<size;i++){
	
		EEPROM.write(address + i, data[i]);
	
	}
	
	if (EEPROM.commit()) {
		return MEM_OK;
	} else {
		return MEM_KO;
	}

}
Flash_Error MemoryFoam::read_memory(int address, uint8_t * data, int size){

		
		int i=0;

		for (i=0;i<size;i++){

			data[i] = EEPROM.read(address++);

		}

	return MEM_OK;
}
Flash_Error MemoryFoam::clear_memory(int size){
  
  int i=0;
  
  for (i=0;i<size;i++){
  
    EEPROM.write(i, 0x00);
  
  }
  
  if (EEPROM.commit()) {
    return MEM_OK;
  } else {
    return MEM_KO;
  }

}
Flash_Error MemoryFoam::start_memory(int size){
    EEPROM.begin(size);

    return MEM_OK;
}
Flash_Error MemoryFoam::stop_memory(){
  EEPROM.end();
  return MEM_OK;
}

Flash_Error MemoryFoam::write_memory_wo_committ(int address, uint8_t * data, int size){
  int i=0;
  
  for (i=0;i<size;i++){
  
    EEPROM.write(address + i, data[i]);
  
  }
}
Flash_Error MemoryFoam::committ(){
  
    if (EEPROM.commit()) {
    return MEM_OK;
  } else {
    return MEM_KO;
  }
}
#if !defined(NO_GLOBAL_INSTANCES) && !defined(NO_GLOBAL_EEPROM)
MemoryFoam MF;
#endif
