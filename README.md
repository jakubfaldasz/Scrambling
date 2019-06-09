# Scrambling
Simple implementation of a protocol for transmission of scrambled images.
It was my project for the Reliability and diagnostics of digital systems.

## What is it about

Basically scramblers were made to eliminate the undesirable patterns in the data (like for example a long sequences of certain values) so that the message would be easier to transfer.
Scramblers can also be treated as pseudo-random generators which means that they are perfect for data encryption.

## How it works

![alt text](https://upload.wikimedia.org/wikipedia/commons/0/03/Scrambler_randomizer_additive.png)

Each scrambler has its own polynomial that is being used to determine which values in the scrambler are used to generate new data. The values are stored in the linear-feedback shift register (LFSR). For example the scrambler that is used in the DVB standard uses the ![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/bb42320e2412bf02011477474a35e9cdd959e2ca) polynomial which means that each scrambled bit is the result from the xor operation of the 14th and the 15th bit in the LFSR. These bits are later xored with the input bits to generate scrambled data.

## Types of scramblers

We determine two types of scramblers  
-Additive  
-Multiplicative 

The additive scramblers are often called synchronous. It means that the contents of the LFSR has to be replaced with its original values after sending every frame.

The multiplicative scramblers are asynchronous or self-synchronizing so there is no need to reload the LFSR with its initial content. 
