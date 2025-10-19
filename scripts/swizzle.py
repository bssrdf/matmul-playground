
for i in range(0, 8):
   print(f"{i*128+27:016b}")


nrow = 128
s1 = set()
s2 = set()
s3 = set()
s4 = set()
for tx in range(128):
# for idx in range(nrow, nrow+32):
   idx = tx % 2 * 4 * nrow + tx // 2 
   idx_s = idx ^ ( (idx & 0b1110000000) >> 7 )
   s1.add(idx)
   s2.add(idx_s)
   if tx % 2 > 0:
     if tx < 64:
        s3.add(idx_s %32)
     else:
        s4.add(idx_s %32)  
   print(tx, ":", f"{idx:03d}", f"{idx_s:03d}", f"{idx % 32:02d}", f"{idx_s % 32:02d}", idx // 128)

print(len(s1), len(s2))

print(len(s3), len(s4))
print(s3)

smem_stride = 16

for tx in range(32):
   logical_offset = (tx % 32) * smem_stride
   swizzled_offset = logical_offset ^ ((logical_offset & 0b10000000) >> 4)
   sw_inter = swizzled_offset 
   swizzled_offset = swizzled_offset ^ ((swizzled_offset & 0b1100000) >> 2)
   if sw_inter != logical_offset:
      print(f"{tx:02d}", f"{logical_offset:04d}", f"{sw_inter:04d}", f"{swizzled_offset:04d}", 
            f"{logical_offset:016b}", f"{sw_inter:016b}", f"{swizzled_offset:016b}" )
