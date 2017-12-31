/*
 * @file:    c_test.c
 * @date:    Dec 17, 2017
 * @author:  Daniel Disler
 * @note This file is for testing purpose
 *
 */

#include<stdio.h>
#include<string.h>

typedef struct {

    char before;
    union {
    unsigned char byte[3];
    uint32_t value;
    struct {
        uint32_t a : 4;
        uint32_t b : 4;
        uint32_t c : 4;
        uint32_t d : 4;
        uint32_t e : 4;
        uint32_t f : 4;

    } field __attribute__((__packed__));
    } data;
    char after;

} bytes_3;


typedef struct {

    char before;
    union {
    unsigned char byte[4];
    uint32_t value;
    struct {
        uint32_t reserved:8;
        uint32_t a : 4;
        uint32_t b : 4;
        uint32_t c : 4;
        uint32_t d : 4;
        uint32_t e : 4;
        uint32_t f : 4;

    } field __attribute__((__packed__));
    } data;
    char after;

} bytes_3_reserved;



#pragma scalar_storage_order big-endian

typedef struct {

    char before;
    union {
    unsigned char byte[3];
    uint32_t value;
    struct {
        uint32_t f : 4;
        uint32_t e : 4;
        uint32_t d : 4;
        uint32_t c : 4;
        uint32_t b : 4;
        uint32_t a : 4;

    } field __attribute__((__packed__));
    } data;
    char after;

} bytes_3Big;


// big endian version.

struct TsDBCP_CSM1_Current_battery
{
    uint32_t timestamp; //!< Used to determine MIA (missing in action) signals.
    union
    {
        struct
        {
            uint64_t  current_CSM1 : 32u; //lint !e46 Invalid Lint errors in C99 compiler.
            uint64_t  errorType_CSM1 : 7u; //lint !e46 Invalid Lint errors in C99 compiler.
            uint64_t  errorIndication_CSM1 : 1u; //lint !e46 Invalid Lint errors in C99 compiler.
            uint64_t  currentUnfiltered_CSM1 : 24u; //lint !e46 Invalid Lint errors in C99 compiler.
        } signals; //!< Represents the signals in the message.
        uint8_t bytes[8];//lint !e46 Invalid Lint errors in C99 compiler. Raw data in one byte segments.
        uint64_t u64;

    } data;
} __attribute__((__packed__)); //!< TI compiler specific struct packing

#pragma scalar_storage_order little-endian

/********************************************************************************************/

// notice this is the same, except opposite order of bitfields

struct TsDBCP_CSM2_Current_battery
{
    uint32_t timestamp; //!< Used to determine MIA (missing in action) signals.
    union
    {
        struct
        {

            uint64_t  currentUnfiltered_CSM1 : 24u; //lint !e46 Invalid Lint errors in C99 compiler.
            uint64_t  errorIndication_CSM1 : 1u; //lint !e46 Invalid Lint errors in C99 compiler.
            uint64_t  errorType_CSM1 : 7u; //lint !e46 Invalid Lint errors in C99 compiler.
            uint64_t  current_CSM1 : 32u; //lint !e46 Invalid Lint errors in C99 compiler.
        } signals; //!< Represents the signals in the message.
        uint8_t bytes[8];//lint !e46 Invalid Lint errors in C99 compiler. Raw data in one byte segments.
        uint64_t u64;
    } data;
} __attribute__((__packed__)); //!< TI compiler specific struct packing


void print (uint8_t *data)
{
    printf("data: 0x");
    uint8_t i;
    for (i = 0; i<8; i++)
        printf("%02x ",data[i]);
    printf("\n");
}

/** Function to set signal raw value in the message based on signal's start bit **/
void setRawSignal(uint64_t rawValue, uint8_t *data, uint8_t startBit, int old)
{

    uint64_t data_cpy = 0;
    uint8_t i;
    //TODO figure out a replacement for memcpy
    if (old)
    {
        memcpy(&data_cpy, data, 8);
    }
    else
    {
        for(i=0; i<8; i++)
        {
            data_cpy += ((uint64_t)data[i])<<(8*(7-i));
        }
    }

    rawValue = (rawValue << startBit);
    data_cpy |= rawValue;
    if (old)
    {
        memcpy(data, &data_cpy, sizeof(data_cpy));
    }
    else
    {
        for(i=0; i<8; i++)
        {
            data[i] = data_cpy >> (8*(7-i));
        }
    }
}

void test(void)
{
    uint8_t src[8] = {};
    uint32_t timestamp = 0;

    //canFrame_t frame;
    //frame.DLC = 8u;
    //frame.Identifier = 961u;
    //Setting raw value of signal based on start bit

    int old = 0;
    setRawSignal(0xABCDEF, src, 0, old);   //reserved_CSM2 (size 24)
    print (src);
    setRawSignal(0x5A, src, 25, old);   //fail_CSM2 (size 7)
    print (src);
    setRawSignal(1, src, 24, old);   //error_CSM2 (size 1)
    print (src);
    setRawSignal(0x01020304, src, 32, old);   //iString_CSM2 (size 32)
    print (src);

    struct TsDBCP_CSM2_Current_battery littleEndian;
    struct TsDBCP_CSM1_Current_battery bigEndian;
    for (int i = 0; i<8; i++)
    {
        littleEndian.data.bytes[i] = src[7-i];
        bigEndian.data.bytes[i] = src[i];

        printf("%02x",littleEndian.data.bytes[i]);
    }
    printf("\n");
    printf("u64 little:\n%016llx\n", littleEndian.data.u64);
    printf("u64 big:\n%016llx\n", bigEndian.data.u64);

    uint8_t *ptr;
    ptr = &littleEndian.data;
    printf("mem little:\n");
    for (int i = 0; i < 8; i++)
    {
        printf("%02x",*ptr);
        ptr++;
    }
    printf("\n");
    ptr = &bigEndian.data;
    printf("mem big:\n");
    for (int i = 0; i < 8; i++)
    {
        printf("%02x",*ptr);
        ptr++;
    }
    printf("\n");


    printf("\n");
    printf("\n");

    printf("Little Endian\n");
    printf("%x\n",littleEndian.data.signals.current_CSM1);
    printf("%x\n",littleEndian.data.signals.errorType_CSM1);
    printf("%x\n",littleEndian.data.signals.errorIndication_CSM1);
    printf("%x\n",littleEndian.data.signals.currentUnfiltered_CSM1);
    printf("\n");

    printf("Big Endian\n");
    printf("%x\n",bigEndian.data.signals.current_CSM1);
    printf("%x\n",bigEndian.data.signals.errorType_CSM1);
    printf("%x\n",bigEndian.data.signals.errorIndication_CSM1);
    printf("%x\n",bigEndian.data.signals.currentUnfiltered_CSM1);
    printf("\n");



    bytes_3_reserved v3_reserved;
    v3_reserved.data.byte[0]=0x00;
    v3_reserved.data.byte[1]= 0x56;
    v3_reserved.data.byte[2]= 0x34;
    v3_reserved.data.byte[3]= 0x12;
    v3_reserved.before = 0xAA;
    v3_reserved.after = 0x55;


    printf("%x\n",v3_reserved.data.value);
    printf("%x\n",v3_reserved.data.field.a);
    printf("%x\n",v3_reserved.data.field.b);
    printf("%x\n",v3_reserved.data.field.f);


    bytes_3 v3;
    v3.data.byte[0]= 0x56;
    v3.data.byte[1]= 0x34;
    v3.data.byte[2]= 0x12;
    v3.before = 0xAA;
    v3.after = 0x55;


    printf("%x\n",v3.data.value << (8*(sizeof(v3.data) - sizeof(v3.data.byte))));
    printf("%x\n",v3.data.field.a);
    printf("%x\n",v3.data.field.b);
    printf("%x\n",v3.data.field.f);


    bytes_3Big v4;
    v4.data.byte[0]= 0x12;
    v4.data.byte[1]= 0x34;
    v4.data.byte[2]= 0x56;
    v4.before = 0xAA;
    v4.after = 0x55;


    printf("%x\n",v4.data.value);
    printf("%x\n",v4.data.field.a);
    printf("%x\n",v4.data.field.b);
    printf("%x\n",v4.data.field.f);


}

//===========Main function===========
int main(int argc, char **argv)
{
    test();
}



