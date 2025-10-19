
def int_log2(x):
   result = 0
   x >>= 1
   while x > 0:
      result += 1
      x >>= 1
   return result


def swizzle(nrow, ntx, NTHREADS, BK):
   print(int_log2(nrow))
   SWIZZLE_BITS_A = int_log2(nrow) + 2
   
   bit_move = SWIZZLE_BITS_A - int_log2(32//(BK//4)) 
   # bit_move = 3
   bitmask = ((1 << (BK//4-1)) - 1) << SWIZZLE_BITS_A

   print(f"{bitmask:016b}", bit_move)
   for i in range(0, 8):
      print(f"{i*nrow+15:016b}")
   s1 = set()
   s2 = set()
   s3 = set()
   s4 = set()
   b1 = []
   b2 = []
   rowStrideA = (NTHREADS * 4) // BK
   for tx in range(ntx):
   # for idx in range(nrow, nrow+32):
      # idx  = tx % (BK//4) * 4 * nrow + rowStrideA + tx // 2 
      idx  = tx % (BK//4) * 4 * nrow + 0 + tx // (BK//4) 
      idx_s = idx ^ ( (idx & bitmask) >> bit_move)
      s1.add(idx)
      s2.add(idx_s)
      if tx % 2 > 0:
         if tx < 64:
            s3.add(idx_s %32)
         else:
            s4.add(idx_s %32)  
      if tx % 2 == 0:
         b1.append(idx_s % 32)
      else:
         b2.append(idx_s % 32)  
      print(f"{tx:02d}", ":", f"{idx:016b}", f"{idx:04d}", f"{idx_s:016b}", f"{idx_s:04d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}", idx_s // nrow)

   print(len(s1), len(s2))

   print(len(s3), len(s4))
   # print(s3)
   print(b1)
   print(b2)
   tx = 1
   for i in range(8):
   # for idx in range(nrow, nrow+32):
      # idx  = tx % (BK//4) * 4 * nrow + rowStrideA + tx // 2 
      idx  = tx % (BK//4) * 4 * nrow + 0 + tx // (BK//4) + i
      idx_s = idx ^ ( (idx & bitmask) >> bit_move)      
      print(f"{idx:016b}", f"{idx:04d}", f"{idx_s:016b}", f"{idx_s:04d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}")
# swizzle(128, 128, 0b1110000000)
# swizzle(128, 256, 0b1000000000, 5)
# swizzle(128, 256, 256, 16, 0b11000000000, 6)

# swizzle(128, 256, 256, 8)
# swizzle(128, 256, 256, 16)
# swizzle(64, 128,    0b0100000000, 4)
# swizzle(32, 64, 0b10000000, 3)

# swizzle(64, 128, 0b111000000)
# swizzle(32, 64, 0b11100000)
print(int_log2(16))
WARPSIZE = 32

def swizzle2(ntx, WM, WN, WNITER, TM, TN, bitmask, bit_move):
   # print(int_log2(nrow))
   print(bitmask)
   # bit_move = int_log2(nrow) - 1
   # bit_move = 3
   # for i in range(0, 8):
   #    print(f"{i*nrow+15:016b}")
   s1 = set()
   s2 = set()
   s3 = set()
   s4 = set()
   b1 = []
   b2 = []
   WMITER = (WM * WN) // (WARPSIZE * TM * TN * WNITER)   
   WSUBM = WM // WMITER
   WSUBN = WN // WNITER

   nrow = TN * WSUBM 
   subi = 1
   subj = 0
   for tx in range(ntx):
      threadColInWarp = tx % (WSUBN // TN)
      threadRowInWarp = tx // (WSUBN // TN)

   # for idx in range(nrow, nrow+32):
      idx  =  threadColInWarp * TN * WSUBM + threadRowInWarp * TM + subj * WSUBM + subi
      idx_s = idx ^ ( (idx & bitmask) >> bit_move)
      print(f"{tx:02d}", ":", f"{idx:012b}", f"{idx:03d}", f"{idx_s:012b}", f"{idx_s:03d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}", idx // nrow)
   tx = 1
   for i  in range(TM):
      for j  in range(TN):
         threadColInWarp = tx % (WSUBN // TN)
         threadRowInWarp = tx // (WSUBN // TN)
         idx  =  threadColInWarp * TN * WSUBM + threadRowInWarp * TM + j * WSUBM + i
         idx_s = idx ^ ( (idx & bitmask) >> bit_move)
         print(i, j, f"{idx:012b}", f"{idx:03d}", f"{idx_s:012b}", f"{idx_s:03d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}")



swizzle2(32, 64, 32, 2, 4, 4, 0b0110000000, 7)

smem_stride = 16

for tx in range(32):
   logical_offset = (tx % 32) * smem_stride
   swizzled_offset = logical_offset ^ ((logical_offset & 0b10000000) >> 4)
   sw_inter = swizzled_offset 
   swizzled_offset = swizzled_offset ^ ((swizzled_offset & 0b1100000) >> 2)
   if sw_inter != logical_offset:
      print(f"{tx:02d}", f"{logical_offset:04d}", f"{sw_inter:04d}", f"{swizzled_offset:04d}", 
            f"{logical_offset:016b}", f"{sw_inter:016b}", f"{swizzled_offset:016b}" )
