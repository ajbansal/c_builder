from c_builder.c_file_writer import *

filename = r"c_test_autogen.c"
outputpath = r"sample_output"
indent = "    "

with CFile(filename, outputpath, indent) as f:
    f.write("""/*\n""")
    f.write("""* @file:    c_test.c\n""")
    f.write("""* @date:    Dec 17, 2017\n""")
    f.write("""* @author:  Daniel Disler\n""")
    f.write("""* @note This file is for testing purpose\n""")
    f.write("""*\n""")
    f.write("""*/\n""")
    f.write("""#include<stdio.h>\n""")
    f.write("""#include<string.h>\n""")
    f.write("\n")

    with CStruct("", typedef=True, base=f) as Block_level_1:
        Block_level_1.add_code_line(r'char before')

        with CUnion("", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'unsigned char byte[3]')
            Block_level_2.add_code_line(r'uint32_t value')

            with CStruct("", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'uint32_t a : 4')
                Block_level_3.add_code_line(r'uint32_t b : 4')
                Block_level_3.add_code_line(r'uint32_t c : 4')
                Block_level_3.add_code_line(r'uint32_t d : 4')
                Block_level_3.add_code_line(r'uint32_t e : 4')
                Block_level_3.add_code_line(r'uint32_t f : 4')
                Block_level_3.add_instance_var(' field __attribute__((__packed__));')
            Block_level_2.add_instance_var(' data;')
        Block_level_1.add_code_line(r'char after')
        Block_level_1.add_instance_var(' bytes_3;')
    f.write("\n")

    with CStruct("", typedef=True, base=f) as Block_level_1:
        Block_level_1.add_code_line(r'char before')

        with CUnion("", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'unsigned char byte[4]')
            Block_level_2.add_code_line(r'uint32_t value')

            with CStruct("", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'uint32_t reserved:8')
                Block_level_3.add_code_line(r'uint32_t a : 4')
                Block_level_3.add_code_line(r'uint32_t b : 4')
                Block_level_3.add_code_line(r'uint32_t c : 4')
                Block_level_3.add_code_line(r'uint32_t d : 4')
                Block_level_3.add_code_line(r'uint32_t e : 4')
                Block_level_3.add_code_line(r'uint32_t f : 4')
                Block_level_3.add_instance_var(' field __attribute__((__packed__));')
            Block_level_2.add_instance_var(' data;')
        Block_level_1.add_code_line(r'char after')
        Block_level_1.add_instance_var(' bytes_3_reserved;')
    f.write("""#pragma scalar_storage_order big-endian\n""")
    f.write("\n")

    with CStruct("", typedef=True, base=f) as Block_level_1:
        Block_level_1.add_code_line(r'char before')

        with CUnion("", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'unsigned char byte[3]')
            Block_level_2.add_code_line(r'uint32_t value')

            with CStruct("", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'uint32_t f : 4')
                Block_level_3.add_code_line(r'uint32_t e : 4')
                Block_level_3.add_code_line(r'uint32_t d : 4')
                Block_level_3.add_code_line(r'uint32_t c : 4')
                Block_level_3.add_code_line(r'uint32_t b : 4')
                Block_level_3.add_code_line(r'uint32_t a : 4')
                Block_level_3.add_instance_var(' field __attribute__((__packed__));')
            Block_level_2.add_instance_var(' data;')
        Block_level_1.add_code_line(r'char after')
        Block_level_1.add_instance_var(' bytes_3Big;')
    f.write("""// big endian version.\n""")
    f.write("\n")

    with CStruct("TsDBCP_CSM1_Current_battery", base=f) as Block_level_1:
        Block_level_1.add_code_line(r'uint32_t timestamp //!< Used to determine MIA (missing in action) signals.')

        with CUnion("", base=Block_level_1) as Block_level_2:

            with CStruct("", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'uint64_t  current_CSM1 : 32u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_code_line(r'uint64_t  errorType_CSM1 : 7u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_code_line(r'uint64_t  errorIndication_CSM1 : 1u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_code_line(r'uint64_t  currentUnfiltered_CSM1 : 24u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_instance_var(' signals; //!< Represents the signals in the message.')
            Block_level_2.add_code_line(r'uint8_t bytes[8]//lint !e46 Invalid Lint errors in C99 compiler. Raw data in one byte segments.')
            Block_level_2.add_code_line(r'uint64_t u64')
            Block_level_2.add_instance_var(' data;')
        Block_level_1.add_instance_var(' __attribute__((__packed__)); //!< TI compiler specific struct packing')
    f.write("""#pragma scalar_storage_order little-endian\n""")
    f.write("""/********************************************************************************************/\n""")
    f.write("""// notice this is the same, except opposite order of bitfields\n""")
    f.write("\n")

    with CStruct("TsDBCP_CSM2_Current_battery", base=f) as Block_level_1:
        Block_level_1.add_code_line(r'uint32_t timestamp //!< Used to determine MIA (missing in action) signals.')

        with CUnion("", base=Block_level_1) as Block_level_2:

            with CStruct("", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'uint64_t  currentUnfiltered_CSM1 : 24u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_code_line(r'uint64_t  errorIndication_CSM1 : 1u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_code_line(r'uint64_t  errorType_CSM1 : 7u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_code_line(r'uint64_t  current_CSM1 : 32u //lint !e46 Invalid Lint errors in C99 compiler.')
                Block_level_3.add_instance_var(' signals; //!< Represents the signals in the message.')
            Block_level_2.add_code_line(r'uint8_t bytes[8]//lint !e46 Invalid Lint errors in C99 compiler. Raw data in one byte segments.')
            Block_level_2.add_code_line(r'uint64_t u64')
            Block_level_2.add_instance_var(' data;')
        Block_level_1.add_instance_var(' __attribute__((__packed__)); //!< TI compiler specific struct packing')
    f.write("\n")

    with CCodeBlock("void print (uint8_t *data)", base=f) as Block_level_1:
        Block_level_1.add_code_line(r'printf("data: 0x")')
        Block_level_1.add_code_line(r'uint8_t i')
        Block_level_1.add_code_line(r'for (i = 0 i<8 i++)')
        Block_level_1.add_code_line(r'printf("%02x ",data[i])')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'')
    f.write("""/** Function to set signal raw value in the message based on signal's start bit **/\n""")
    f.write("\n")

    with CCodeBlock("void setRawSignal(uint64_t rawValue, uint8_t *data, uint8_t startBit, int old)", base=f) as Block_level_1:
        Block_level_1.add_code_line(r'uint64_t data_cpy = 0')
        Block_level_1.add_code_line(r'uint8_t i')
        Block_level_1.add_code_line(r'//TODO figure out a replacement for memcpy')

        with CIf("(old)", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'memcpy(&data_cpy, data, 8)')
            Block_level_2.add_code_line(r'')

        with CElse(base=Block_level_1) as Block_level_2:

            with CFor("(i=0; i<8; i++)", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'data_cpy += ((uint64_t)data[i])<<(8*(7-i))')
                Block_level_3.add_code_line(r'')
            Block_level_2.add_code_line(r'')
        Block_level_1.add_code_line(r'rawValue = (rawValue << startBit)')
        Block_level_1.add_code_line(r'data_cpy |= rawValue')

        with CIf("(old)", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'memcpy(data, &data_cpy, sizeof(data_cpy))')
            Block_level_2.add_code_line(r'')

        with CElse(base=Block_level_1) as Block_level_2:

            with CFor("(i=0; i<8; i++)", base=Block_level_2) as Block_level_3:
                Block_level_3.add_code_line(r'data[i] = data_cpy >> (8*(7-i))')
                Block_level_3.add_code_line(r'')
            Block_level_2.add_code_line(r'')
        Block_level_1.add_code_line(r'')
    f.write("\n")

    with CCodeBlock("void test(void)", base=f) as Block_level_1:
        Block_level_1.add_code_line(r'uint8_t src[8] = {}')
        Block_level_1.add_code_line(r'uint32_t timestamp = 0')
        Block_level_1.add_code_line(r'//canFrame_t frame')
        Block_level_1.add_code_line(r'//frame.DLC = 8u')
        Block_level_1.add_code_line(r'//frame.Identifier = 961u')
        Block_level_1.add_code_line(r'//Setting raw value of signal based on start bit')
        Block_level_1.add_code_line(r'int old = 0')
        Block_level_1.add_code_line(r'setRawSignal(0xABCDEF, src, 0, old)   //reserved_CSM2 (size 24)')
        Block_level_1.add_code_line(r'print (src)')
        Block_level_1.add_code_line(r'setRawSignal(0x5A, src, 25, old)   //fail_CSM2 (size 7)')
        Block_level_1.add_code_line(r'print (src)')
        Block_level_1.add_code_line(r'setRawSignal(1, src, 24, old)   //error_CSM2 (size 1)')
        Block_level_1.add_code_line(r'print (src)')
        Block_level_1.add_code_line(r'setRawSignal(0x01020304, src, 32, old)   //iString_CSM2 (size 32)')
        Block_level_1.add_code_line(r'print (src)')
        Block_level_1.add_code_line(r'struct TsDBCP_CSM2_Current_battery littleEndian')
        Block_level_1.add_code_line(r'struct TsDBCP_CSM1_Current_battery bigEndian')

        with CFor("(int i = 0; i<8; i++)", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'littleEndian.data.bytes[i] = src[7-i]')
            Block_level_2.add_code_line(r'bigEndian.data.bytes[i] = src[i]')
            Block_level_2.add_code_line(r'printf("%02x",littleEndian.data.bytes[i])')
            Block_level_2.add_code_line(r'')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'printf("u64 little:\n%016llx\n", littleEndian.data.u64)')
        Block_level_1.add_code_line(r'printf("u64 big:\n%016llx\n", bigEndian.data.u64)')
        Block_level_1.add_code_line(r'uint8_t *ptr')
        Block_level_1.add_code_line(r'ptr = &littleEndian.data')
        Block_level_1.add_code_line(r'printf("mem little:\n")')

        with CFor("(int i = 0; i < 8; i++)", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'printf("%02x",*ptr)')
            Block_level_2.add_code_line(r'ptr++')
            Block_level_2.add_code_line(r'')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'ptr = &bigEndian.data')
        Block_level_1.add_code_line(r'printf("mem big:\n")')

        with CFor("(int i = 0; i < 8; i++)", base=Block_level_1) as Block_level_2:
            Block_level_2.add_code_line(r'printf("%02x",*ptr)')
            Block_level_2.add_code_line(r'ptr++')
            Block_level_2.add_code_line(r'')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'printf("Little Endian\n")')
        Block_level_1.add_code_line(r'printf("%x\n",littleEndian.data.signals.current_CSM1)')
        Block_level_1.add_code_line(r'printf("%x\n",littleEndian.data.signals.errorType_CSM1)')
        Block_level_1.add_code_line(r'printf("%x\n",littleEndian.data.signals.errorIndication_CSM1)')
        Block_level_1.add_code_line(r'printf("%x\n",littleEndian.data.signals.currentUnfiltered_CSM1)')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'printf("Big Endian\n")')
        Block_level_1.add_code_line(r'printf("%x\n",bigEndian.data.signals.current_CSM1)')
        Block_level_1.add_code_line(r'printf("%x\n",bigEndian.data.signals.errorType_CSM1)')
        Block_level_1.add_code_line(r'printf("%x\n",bigEndian.data.signals.errorIndication_CSM1)')
        Block_level_1.add_code_line(r'printf("%x\n",bigEndian.data.signals.currentUnfiltered_CSM1)')
        Block_level_1.add_code_line(r'printf("\n")')
        Block_level_1.add_code_line(r'bytes_3_reserved v3_reserved')
        Block_level_1.add_code_line(r'v3_reserved.data.byte[0]=0x00')
        Block_level_1.add_code_line(r'v3_reserved.data.byte[1]= 0x56')
        Block_level_1.add_code_line(r'v3_reserved.data.byte[2]= 0x34')
        Block_level_1.add_code_line(r'v3_reserved.data.byte[3]= 0x12')
        Block_level_1.add_code_line(r'v3_reserved.before = 0xAA')
        Block_level_1.add_code_line(r'v3_reserved.after = 0x55')
        Block_level_1.add_code_line(r'printf("%x\n",v3_reserved.data.value)')
        Block_level_1.add_code_line(r'printf("%x\n",v3_reserved.data.field.a)')
        Block_level_1.add_code_line(r'printf("%x\n",v3_reserved.data.field.b)')
        Block_level_1.add_code_line(r'printf("%x\n",v3_reserved.data.field.f)')
        Block_level_1.add_code_line(r'bytes_3 v3')
        Block_level_1.add_code_line(r'v3.data.byte[0]= 0x56')
        Block_level_1.add_code_line(r'v3.data.byte[1]= 0x34')
        Block_level_1.add_code_line(r'v3.data.byte[2]= 0x12')
        Block_level_1.add_code_line(r'v3.before = 0xAA')
        Block_level_1.add_code_line(r'v3.after = 0x55')
        Block_level_1.add_code_line(r'printf("%x\n",v3.data.value << (8*(sizeof(v3.data) - sizeof(v3.data.byte))))')
        Block_level_1.add_code_line(r'printf("%x\n",v3.data.field.a)')
        Block_level_1.add_code_line(r'printf("%x\n",v3.data.field.b)')
        Block_level_1.add_code_line(r'printf("%x\n",v3.data.field.f)')
        Block_level_1.add_code_line(r'bytes_3Big v4')
        Block_level_1.add_code_line(r'v4.data.byte[0]= 0x12')
        Block_level_1.add_code_line(r'v4.data.byte[1]= 0x34')
        Block_level_1.add_code_line(r'v4.data.byte[2]= 0x56')
        Block_level_1.add_code_line(r'v4.before = 0xAA')
        Block_level_1.add_code_line(r'v4.after = 0x55')
        Block_level_1.add_code_line(r'printf("%x\n",v4.data.value)')
        Block_level_1.add_code_line(r'printf("%x\n",v4.data.field.a)')
        Block_level_1.add_code_line(r'printf("%x\n",v4.data.field.b)')
        Block_level_1.add_code_line(r'printf("%x\n",v4.data.field.f)')
        Block_level_1.add_code_line(r'')
    f.write("""//===========Main function===========\n""")
    f.write("\n")

    with CCodeBlock("int main(int argc, char **argv)", base=f) as Block_level_1:
        Block_level_1.add_code_line(r'test()')
        Block_level_1.add_code_line(r'')
