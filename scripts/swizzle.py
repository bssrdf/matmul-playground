
def int_log2(x):
   result = 0
   x >>= 1
   while x > 0:
      result += 1
      x >>= 1
   return result


def swizzle(nrow, ntx, NTHREADS, BK):
   print(int_log2(nrow))
   # SWIZZLE_BITS_A = int_log2(nrow) + 2   
   # bit_move = SWIZZLE_BITS_A - int_log2(32//(BK//4)) 
   # bit_move = SWIZZLE_BITS_A - 3
   # bitmask = ((1 << (BK//4-1)) - 1) << SWIZZLE_BITS_A

   SWIZZLE_BITS_A = int_log2(nrow)
   # bit_move = SWIZZLE_BITS_A - int_log2(32//(BK//4)) 
   bit_move = SWIZZLE_BITS_A - 3
   bitmask = ((1 << (3)) - 1) << SWIZZLE_BITS_A

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
      idx1  = tx % (BK//4) * 4 * nrow + nrow + tx // (BK//4) 
      idx1_s = idx1 ^ ( (idx1 & bitmask) >> bit_move)
      # s1.add(idx)
      # s2.add(idx_s)
      # if tx % 2 > 0:
      #    if tx < 64:
      #       s3.add(idx_s %32)
      #    else:
      #       s4.add(idx_s %32)  
      # if tx % 2 == 0:
      #    b1.append(idx_s % 32)
      # else:
      #    b2.append(idx_s % 32)  
      print(f"{tx:02d}", ":", f"{idx:016b}", f"{idx:04d}", f"{idx_s:016b}", f"{idx_s:04d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}", idx_s // nrow)
      # print(f"{tx:02d}", ":", f"{idx:016b}", f"{idx:04d}", f"{idx_s:016b}", f"{idx_s:04d}", f"{idx_s % 32:02d}", f"{idx_s//nrow:01d}", 
      #       f"{idx1:016b}", f"{idx1:04d}", f"{idx1_s:016b}", f"{idx1_s:04d}", f"{idx1_s % 32:02d}", f"{idx1_s//nrow:01d}")

   # print(len(s1), len(s2))

   # print(len(s3), len(s4))
   # # print(s3)
   # print(b1)
   # print(b2)
   # tx = 1
   # for i in range(8):
   # # for idx in range(nrow, nrow+32):
   #    # idx  = tx % (BK//4) * 4 * nrow + rowStrideA + tx // 2 
   #    idx  = tx % (BK//4) * 4 * nrow + 0 + tx // (BK//4) + i
   #    idx_s = idx ^ ( (idx & bitmask) >> bit_move)      
   #    print(f"{idx:016b}", f"{idx:04d}", f"{idx_s:016b}", f"{idx_s:04d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}")
# swizzle(128, 128, 0b1110000000)
# swizzle(128, 256, 0b1000000000, 5)
# swizzle(128, 256, 256, 16, 0b11000000000, 6)

# swizzle(128, 256, 256, 8)
# swizzle(128, 32, 256, 8)
# swizzle(128, 256, 256, 16)
# swizzle(64, 128,    0b0100000000, 4)
# swizzle(32, 64, 0b10000000, 3)

# swizzle(64, 128, 0b111000000)
# swizzle(32, 64, 0b11100000)
# print(int_log2(16))
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



# swizzle2(32, 64, 32, 2, 4, 4, 0b0110000000, 7)

smem_stride = 16

# for tx in range(32):
#    logical_offset = (tx % 32) * smem_stride
#    swizzled_offset = logical_offset ^ ((logical_offset & 0b10000000) >> 4)
#    sw_inter = swizzled_offset 
#    swizzled_offset = swizzled_offset ^ ((swizzled_offset & 0b1100000) >> 2)
#    if sw_inter != logical_offset:
#       print(f"{tx:02d}", f"{logical_offset:04d}", f"{sw_inter:04d}", f"{swizzled_offset:04d}", 
#             f"{logical_offset:016b}", f"{sw_inter:016b}", f"{swizzled_offset:016b}" )
def swizzle3(ntx, BK):
   
   for tx in range(ntx):
      idx = tx // 4 * 4 * BK + tx % 4 * BK 
      idx_s = idx ^ ( (idx & 0b00011100000) >> 5)
      idx1 = tx // 4 * 4 * BK + tx % 4 * BK + 1; 
      idx1_s = idx1 ^ ( (idx1 & 0b00011100000) >> 5)
      idx_s1 = idx_s ^ 1
      idx2 = tx // 4 * 4 * BK + tx % 4 * BK + 2; 
      idx2_s = idx2 ^ ( (idx2 & 0b00011100000) >> 5)
      idx_s2 = idx_s1 ^ 3
      idx3 = tx // 4 * 4 * BK + tx % 4 * BK + 3; 
      idx3_s = idx3 ^ ( (idx3 & 0b00011100000) >> 5)
      idx_s3 = idx_s2 ^ 1
      idx4 = tx // 4 * 4 * BK + tx % 4 * BK + 4; 
      idx4_s = idx4 ^ ( (idx4 & 0b00011100000) >> 5)
      idx_s4 = idx_s3 ^ 7
      idx5 = tx // 4 * 4 * BK + tx % 4 * BK + 5; 
      idx5_s = idx5 ^ ( (idx5 & 0b00011100000) >> 5)
      idx_s5 = idx_s4 ^ 1
      idx6 = tx // 4 * 4 * BK + tx % 4 * BK + 6; 
      idx6_s = idx6 ^ ( (idx6 & 0b00011100000) >> 5)
      idx_s6 = idx_s5 ^ 3
      idx7 = tx // 4 * 4 * BK + tx % 4 * BK + 7; 
      idx7_s = idx7 ^ ( (idx7 & 0b00011100000) >> 5)
      idx_s7 = idx_s6 ^ 1
      # print(f"{tx:02d}", f"{idx:016b}", f"{idx:03d}", f"{idx_s:016b}", f"{idx_s:03d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}",
      #       f"{idx_s1:016b}", f"{idx_s1:03d}", f"{idx_s1 % 32:02d}")
      # print(f"{tx:02d}", f"{idx1_s:016b}", f"{idx1_s:03d}", f"{idx1_s % 32:02d}", f"{idx_s1:016b}", f"{idx_s1:03d}", f"{idx_s1 % 32:02d}")
      # print(f"{tx:02d}", f"{idx2_s:016b}", f"{idx2_s:03d}", f"{idx2_s % 32:02d}", f"{idx_s2:016b}", f"{idx_s2:03d}", f"{idx_s2 % 32:02d}")
      # print(f"{tx:02d}", f"{idx3_s:016b}", f"{idx3_s:03d}", f"{idx3_s % 32:02d}", f"{idx_s3:016b}", f"{idx_s3:03d}", f"{idx_s3 % 32:02d}")
      # print(f"{tx:02d}", f"{idx4_s:016b}", f"{idx4_s:03d}", f"{idx4_s % 32:02d}", f"{idx_s4:016b}", f"{idx_s4:03d}", f"{idx_s4 % 32:02d}")
      # print(f"{tx:02d}", f"{idx5_s:016b}", f"{idx5_s:03d}", f"{idx5_s % 32:02d}", f"{idx_s5:016b}", f"{idx_s5:03d}", f"{idx_s5 % 32:02d}")
      # print(f"{tx:02d}", f"{idx6_s:016b}", f"{idx6_s:03d}", f"{idx6_s % 32:02d}", f"{idx_s6:016b}", f"{idx_s6:03d}", f"{idx_s6 % 32:02d}")
      print(f"{tx:02d}", f"{idx7_s:016b}", f"{idx7_s:03d}", f"{idx7_s % 32:02d}", f"{idx_s7:016b}", f"{idx_s7:03d}", f"{idx_s7 % 32:02d}")

# swizzle3(32, 8)

def swizzle4(ntx, BM):
   SWIZZLE_MASK_1 = 0b10000
   SWIZZLE_BITS_1 = 4
   SWIZZLE_MASK_2 = 0b1100
   SWIZZLE_BITS_2 = 2
   TILE_COLS_VECTORIZED = 4
   ROW_STEP = ntx // TILE_COLS_VECTORIZED
   NUM_ITERS = BM // ROW_STEP
   thread_row = [0]*ntx
   thread_col = [0]*ntx
   for tx in range(ntx):
      thread_row[tx] = tx // TILE_COLS_VECTORIZED
      thread_col[tx] = tx % TILE_COLS_VECTORIZED
   for i in range(NUM_ITERS):
      for tx in range(ntx):
         dst_index = thread_row[tx] * TILE_COLS_VECTORIZED + thread_col[tx]
         idx = dst_index
         dst_index = dst_index ^ ((dst_index & SWIZZLE_MASK_1) >> SWIZZLE_BITS_1)
         idx1 = dst_index
         dst_index = dst_index ^ ((dst_index & SWIZZLE_MASK_2) >> SWIZZLE_BITS_2)
         # idx_s = idx ^ ((idx & 0b00011100000) >> 5)
         print(f"{tx:03d}", f"{thread_row[tx]:02d}", f"{thread_col[tx]:02d}", f"{i:02d}", 
               f"{idx:04d}", f"{idx:016b}",f"{idx1:04d}", f"{idx1:016b}", f"{dst_index:03d}", f"{dst_index:016b}")
      for tx in range(ntx):
         thread_row[tx] += ROW_STEP
# swizzle4(256, 256)
def swizzle5(ntx, smem_stride):
   for tx in range(ntx):
      logical_offset = (tx % 32) * smem_stride
      swizzled_offset = logical_offset ^ ((logical_offset & 0b10000000) >> 4)
      swizzled_offset = swizzled_offset ^ ((swizzled_offset & 0b1100000) >> 2)
      print(f"{tx:03d}", f"{logical_offset:04d}", f"{logical_offset//8:03d}", f"{logical_offset:016b}", 
            f"{swizzled_offset:04d}", f"{swizzled_offset//8:03d}", f"{swizzled_offset:016b}", 
            f"{((swizzled_offset*2)^ 0b10000)//2:03d}")

# swizzle5(32, 32)

def swizzle6(ntx):

   for tx in range(32):
      row = 32
      print(f"{tx:02d}", end=':')
      # print(f"{tx:02d}",  f"{idx0:02d}", f"{idx0:016b}", f"{idx:02d}", f"{idx:016b}",)
      for col in range(32):
         idx = row * tx + col 
         idx0 = idx
         # idx = idx ^ ((idx & 0b1111100000) >> 5)
         idx = col ^ tx
         print(f"{idx%32:02d}", end=',')
      print()

idx = 32 * 1 + 5
print(f"{idx:03d}", f"{idx:016b}")
idx = 32 * 31 + 5
print(f"{idx:03d}", f"{idx:016b}")

swizzle6(32)


def swizzle7(ntx, BN, WN):
   warp_n = 0
   mma_m = 0
   mma_n = 0
   MMA_M = 16
   MMA_N = 8 
   mma_tiles_per_warp_n = 8
   i = 0
   for lane_id in range(32):
      mma_row = lane_id // 4
      mma_col = lane_id % 4
      output_sts_addr = (mma_row * BN//2 + warp_n * WN//2  + mma_col * 2 +  
                         mma_m * MMA_M * BN // 2 + (mma_n - i * mma_tiles_per_warp_n//2) * MMA_N)
      idx = output_sts_addr ^ ((output_sts_addr & 0b1110000000) >> 4)
      print(f"{lane_id:02d}", f"{output_sts_addr:04d}", f"{output_sts_addr//(BN//2):03d}", f"{(output_sts_addr//2)%32:02d}", f"{output_sts_addr:016b}",
            f"{idx:04d}", f"{idx//(BN//2):03d}", f"{(idx//2)%32:02d}", f"{idx:016b}")   

swizzle7(32, 256, 64)
