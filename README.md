# Scrambling
Simple implementation of a protocol for transmission of scrambled images.
It was a project for the Reliability and diagnostics of digital systems.

## Something about scramblers

Basically scramblers were made to eliminate the undesirable patterns in the data (like for example a long sequences of certain values) so that the message would be easier to transfer.
Scramblers can also be treated as pseudo-random generators which means that they can also be used to encrypt data.

## How it works

![alt text](https://upload.wikimedia.org/wikipedia/commons/0/03/Scrambler_randomizer_additive.png)

Each scrambler has its own polynomial that is being used to determine which values in the scrambler are used to generate new data. The values are stored in the linear-feedback shift register (LFSR). For example the scrambler that is used in the DVB standard uses the ![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/bb42320e2412bf02011477474a35e9cdd959e2ca) polynomial which means that each scrambled bit is the result from the xor operation of the 14th and the 15th bit in the LFSR. These bits are later xored with the input bits to generate scrambled data as in the picture above.

# Example

In this example we will try to scramble the 8-bit grayscale image of the Golden Gate bridge. The image was loaded and converted to list of pixel values using the OpenCV library.
 
<img src="https://i.imgur.com/tZHj3H4.jpg" width="400">

```python
scramble_image(self, input_image, output_image)
```
After using the method from above, our scrambled image looks like this  

<img src="https://i.imgur.com/PCsA5GI.png" width="400">

## Types of scramblers

We determine two types of scramblers  
-Additive  
-Multiplicative 

The additive scramblers are often called synchronous. It means that the contents of the LFSR has to be replaced with its original values after sending each frame.

The multiplicative scramblers are asynchronous (self-synchronizing) so there is no need to reload the LFSR with its initial content. 

## Transmission protocol

I've implemented a simple protocol for transmitting data between the Transmitter class and the Receiver. 

To simplify things the Receiver doesn't ask for retransmission if the frame was corrupted and also the whole data is being framed at once in the Transmitter class. 

In the generate_output(self, image_name) method the image is converted to binary data and is later scrambled. Then we take every 320 bits of our scrambled data and we form it into frames. It means that the syncword is attached at the beginning of every frame. In order to check if the data that was sent wasn't corrupted we count the 32 bits Cyclic Redundancy Check (CRC-32). These bits are also attached to the frame.

In the Receiver class we decode the data by looking for the sync word and by synchronising our descrambler. Later we check if the data and the CRC match. If not the frame is rejeceted. 

In the example below we've used a DVB scrambler, 10bits long syncword. The transmitted data was 320 bits long. Generated data was then intentionally corrupted by randomly negating of individual bits.

Finally the received image looked like this  

<img src="https://i.imgur.com/UaW5Y6c.png" width="400">
