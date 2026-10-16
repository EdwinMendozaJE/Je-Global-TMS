import streamlit as st
import pandas as pd
import datetime
import base64

# Page Configuration - Clean Streamlit Theme
st.set_page_config(
    page_title="JE Global Logistics LLC - TMS Portal",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Company Logo Base64
LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAC/AV4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD66oopDQAtFJmigQtFFJQAtFJmigYtFFFArhRRRQFwopM0ZoGLRTc0tAC0UgpaACiiigAoowaMUAFFGKKACiiigAoopKAFoptFADqKTNGaAFopKWgQUUUUBcKKKKAuFFJRmgYtJRmkoAWkNFFADqaadTaAAdaWkpaAFopKKACiiigBaSikoAWjNJRQAUUUUAKKWkFLQAUVQ8Qa1pPh7SJ9Y1zUbbTtPt13S3FxIERfxPU+gHJryIfEL4h/Ex2g+Euhx6PoJO0+KtchIWQettB1f2ZuPUCgD1/WtW0rRLB9Q1rU7PTbRBlp7qdYkH4sQK8vvv2hPAj3b2PhW18QeNLxDgxaFpkky5/322r+IzT9C+AvhZr9NZ8eX+p+Ptb6m41mYtAh9I4Adir7HNbsfxN+FmheJrPwJZ+ItGtNTmn+yRafZoAkcvTYxQbEORjBIOcCgDnB8Q/jJqjZ0L4Hy2kTfdl1rW4oD+MYG6nHU/2kZvmj8K/Dq2H92TUrhyPyFb37QHxHl+Ffw/bxVHoo1fF3HbGA3Hkhd4b5i21u4AxjvXZeGtSXWvDel6yiBFv7OG6CA5C+YgbGe+M0AeX/ANs/tG2w3TeCPAV+B/Db6tLGx+hcYpjfFX4jaQC3ir4GeIo4l+9Not7FfjHrtXBr1LxLqsOheHNT1u5GYdPs5bpxnGRGhYjPbpXJ/Aj4jD4peAk8VposukI11JbrC84l3bMZYMAOMkjp2oAy/Dfx6+GOsXo064159B1LIBs9bt2spAT2y425/wCBV6ZDJHNCk0MiSxOMo6MGVh6gjg1keLtB8K+IbRbLxVpWkajDKdqJfxIxJ/2S3IP05rzS5+Cmo+FJnv8A4PeMtQ8Ky53HSL12u9MmPXBR8smfUZoA9lorx7QvjJdaFq8Hhv4xaAfB+qTNsttTRjJpd6f9iX/lmfZuncivYEZXRZEZXRgGVlOQwPQg9xQAUlOpKAEopSKMUAJSikooAdRSUUCsLSUnvRmgYuKSlpDQAUUUUAFFFFADqbTqQ0AJSikooAWkNFFABRRRQAUUUUAFFFFABS4oFLQAlcb8VfiLovw+0uCS9jn1DVr9/J0vSbQbrm9l6BVXsuSMt0HucCnfFzx/p3w98L/2ncwSX2o3UgttL02HmW9uW4WNQOcZxk9h7kA898IPh1qGnanP8Q/iHPFqXjrUUzI55h0qEji3gHRQBwzDrzz1JAMrwx8L9b8a6vb+MvjVJFf3UbeZp3hmJs6fpo7bx0mlx1JyPrxix8VPjt4d8H6kvhLwtp03i3xcT5MOkaau5YW6ASMoO3H90Akd8da5Dx7+1j4d0PxDcWfh3wxqHiXSbCZYtQ1WCXy4UYnGIztIbkHBJUNjjjmvNP2hv+JXqmlftDfCDW5rTTdeRrTVLizUb7eZhhiyn7rMBgg9HUHOWBoA95/Zt+LWu/EW88SaF4s8Ox6Hr+gXCpcQxBghViw2kMSQylSDzyCDXx74tg8HXXiv4uNr2qnTdeh1pp9AdInd5ZluJt8fyA4DArycYO09q6/wvoVrq/xl8MXHwGvfFGs3lhOtz4h8QakxSCZmYMxfPQbS6kHls4Gep+nPhX8E9J8FePPFPjG8vLfWb7XL2S4hWWyUCyVpHfCMSTuO4AkY6UAeC+JviiPir+x74h0/WJQPFXh17Rr5G4a4QToizgep3Yb0b6iu7+Bf7R/gl/DfgjwK1prs2s/ZrTS5JFtV8lJcLGCW3525xziveLTwV4PtNS1HUrfwvo6XupsXvp/saF7gkgncSORkA46ZGetbFtZWVqALaztoAOgihVcfkKAPLf2vtb/sL9nrxRIG2yXkUdinPXzZFVh/3zurm/2Q/HPw6t/hR4W8F2XirTv7eETtPYyExymZ3Z2UBgNxAPbPSvdr6zs7+2a2vrS3u4G+9FPEsiH6hgRXK2fwt+HVl4ltfElh4M0ey1a0cvDc2sAhKkqVJKphTwSORQB8weF/C4/af+N/i3Xte1HU7fwpoo+y6atrIFZTkiILuBAyFaRuM5Irrv2VNe8Tab8aPGHwsPiS68T+GNDjk+zXl0dzwOkioFDEnAOWUrnGVyMc1c1f4C/ETwPrmp6p8C/HMekWeqMWuNKvj8iE5+4xVgcZOCQGHqa838e+H/EPwD+EMPhW2vopvGHj++aPUtThchYYE2jyUkbByxkOWOOGb2NAH1a/iD4afEBr/wAHNrPh3xG2Ct1pvnpMeOp256j1Xkeorze50vxf8CHa/wDDgvvFXw2UlrrSHYyXujr3eBjzJEO6np+bV5D4m+Efw/8AC1hbeBdF1a/sPjDY2sWoWeoNcNbW9/OxBaCJ2ITIGQuMEnAyTuA+n/hh4g1aL4b+FZPiRPb6X4l1FBbSQ3TrFJPPltqhf77KoYqO5NAHReE/EWi+K/D9pr/h7UIdQ027TdFNGfzUjqrA8EHkGtWvCfGugal8F/Ed18RvA1lJceEruTzPFHh6EfLEO95br0Vl6so4x7fd9o0DV9M1/RLPW9GvI7zT72ITW88ZyHU/yPYjqCCKAL1IaWigBtFKaSgApaSloAKSlNJQAUUUUAFFFFABRRRQA6kPWikoAKXtSUUAFFLSUAFFFKRQAlFFFABSikpaAFqtqt/ZaVpl1qeo3KW1laQtPcTOcLGijLMfoBVmvFvjzLP458aeHvgvpszpb6hjVPEksZwYtPib5Y89jI4A/AdjQBF8GdLvfiN4xl+NXii2dLYhrfwhp8w4tLTJBuSP+eknPPpnttx6Z8T9E1DxL8OfEPh/SbsWl/qOnTW9vMWKhXZSBkjoD0J9DUnjFdb03wHqEPgbTrSXV7eyMel2sjCOJWA2oOeMKOgOAcAZGa8U+En7SdvNq3/CGfF3Tz4R8T27CJp50MVtM3+1n/VE+pyp7EcCgDgf2dPiZ4I8EeBde+EPxb0aLQ5rJ5/tSz2zOL8MctG4UEmQcBT0K7cEY50v2NvAya/4b8fpqGm3f/CudfnEOm2V653ShXb94COhVdi7x1YdflrqvCVz4N/aC+KfiK61P4eaXqnhvQClvY69I7pLcyA/cYKQJEPLAH7q4z96voeztraytIbOzt4ra2gQRxQxIFSNQMBVA4AHpQBS8M6BonhnRodG8P6Xa6Zp8IwkFvGFX6n1J7k5JrSorM1bXLDTiUkkMk3/ADzTk/j6VzYvGUMHTdWvNRiurNKVKdWXLBXZp0V5f43+Kth4aghm1fULPSI7glbdZAXlmI7IoBLdR0Hes/xj49v/AAv4JXxlrzatZaW80cKB7fZMTJ90+WcMBx3wfavnlxVTra4XD1Ki7qNl97sd39myj/EnGL7N6nsFFeW+M/Gd/wCBbeK98S3lzaWEhCi9a3MtupPQO6g7M/7WK3NB8dRahp9vfDybuyuU3w3Vq4KuvqOxoXFmGptLF0p0r9ZR0+9XB5ZUkr0pRl6PU7VmVVLMwVR1JOBXEfFbwr4F+I3hiTw54plgkh3b4JopQJbaTGA6Nzg+oPBHBFdFbQ6Nq8fnAi89RK5JX/gPb8qzfEnhyzSwlu7GPyXiG5kBO1h3+hrfMcxzCGGeKwUITilf4m215WSX4kUKFB1PZ1m0/T+vyPmLxL8J9O+HM9p8Qfiv8Q5/GXhrQMQ6FpnztLcSctFAdxKqoxkgHBC84HFQaJpOqfEm+l+Pvx0u5dH8FaViXSdLQsPMXcNgRRztLbefvSH0Wve9P07TNalGi61p9tqWmXjBZ7W4jDxuQdykg9wQDmvDfim/l/Gb4h+Bvid4mn0nw34j0hZfD0kp/wBCheEq1uR/c2FXUhcZOQeoquG89WdYR1uXlknZr7np94swwTwlXkvdPU9p+DHx68EfFjVL3RNMgvLC/iRnS01BEzcw9GZdpIOM8qeceozWF4cVvgl8WI/CjsU+H/i+5Z9HZj8ml6geWt89kf8Ah98ejGvG/hHpPiv4o6d8MfE3he20+wvvBWonStW1FMRM1qmySNj03r5ZdCMZy3PDcfVPxO8MaN8UPh3qmgRXttMs277JdwShxbXUZ+Rwyngqwwe+CRX0JwnYkYNFee/s/eM7zxl8PozrSmLxHo876XrUTfeW5i4LH/eGG+pPpXoVACGkpaDQAUGkooAKKKKACiiigAooooAKKKKAHU2nU00AFAoooAKKUUUAJRS0lABRRQKAFpaSgUANmlighknncRxRqXkc9FUDJJ+grx39mSCXxD/wlHxZv42+1eLNScWO4HMenwExwqPTOCT64BrY/ai1y40L4HeIWsi323UY00y1Cn5i9w4j499pY/hXbeB9Cg8L+DtF8O2ygRaZZQ2wx3KKAT+JyfxoA8F1/wAc+PfGnx+1TSPCfiIaF4I8EFJPEFygXdcBSWmUEqcn5XQDgDaT6VwVr490z44eJ9L8GfFfwD9hXX2kbwxr1mhhuIoyziMEtkSLldpPTI5XuOq8YfCL4v8Aw++IGu+N/gzq9vfWms3D3V7pFwV3MzMWKlZPlkALNggqwBxV74MeEPiX4y+Mtr8Svil4ct/DtvoFibTSNOii8pPMORuWPcSANzsSepK44FAHuPww8FaP8PfBGn+FNEQ/ZrRPnlYAPPKeXkbHcn8hgdq6aisPxhqp0+xEELYuJ8hSOqr3P9K4sxx9LL8NPE1fhivv7L5vQ2oUZV6ipx3ZQ8U+IZEaSx0sSSOikyvEhduBkqgHJP0/CvKvCfxp+EbaPq2p6pq81vqelpJJLpepQGCdymflRW4diccZyM8gV7L4T0hdPtBPMv8ApUoyxP8AAP7v+NeCftKeG9F+I/x18D/DeLTLQXTq+p65qEUSrcLaLkCPzAM4ba3XuUr57LcnnjprMMzXNN6xg/hgumnV92zuxGKjRXsMNour6v8A4Bsfs9+C9Q8Yay/xx+Ilss2r6n82gWMgzFplp/AyKeAxHQ+h3dW4s/t0f8kGl/7C9n/6E1QL+z9qXh4t/wAK4+MXinw1CD8lncSi6gT2C5Xj6g1yXxb+En7QniTwY2iXHxD0fxdafaYpfsptY7aQlScOXKjp6bua+tWmh5Z9Q3Vpaahpb2F/bQ3VpcQ+XNDMgZJEIwVYHgivm7S4k/Z++K0XhXVJRJ8L/FszPp0l02U0m77oWPRTwM+hB6q2d/8A4V9+0FqKrHqnx207T4sYI07Sk3Y9AcJ/Osbxp+zDba54W1ObVfiF4k8UeJ/sztp82o3oECTAZUbDnAOMdeM5qZwjUi4yV0xptO6N21+J/ga/+IkfhrwHq19rF7tZ5JrG1eW2h2jOGlAwQeecFfevUv7dW+8L3s0ibJkTy2A6EtwCP8KyPgVoT+GPhlo2mahoGlaDq0duI7+Gx8vbLIp2+YWT7xYANyTyTUnjKW3in/s2zjVF3+dOF7uRx+n86+CzvCR4fo1MThJ8tOaacOnM1ZOPbu/JHtYOq8dONOqryTvzeS3uQ+B7Uz60JsfJbqXJ9zwP8+1aPxL+Hfgz4iaZDZeMdHjv4rVjJDIJGjki/vbXUggHHI6HFavhexi03TFV3j8+X55PmHB7D8K2Bwc17PCOVSyzLIQqK0pe8/V9PkrfM5c0xKxGIco7LRHzHr37QHwo8DaKPAfwu8LyeJTteCOy0+FktnZhhsuQXlJ7kA59ayf2Htc1jwz4m8QfCrxTplzo1zKo1fTrK6BV4wwG9BnnlCjevyt716F4s8dfA74C6xc2Y0iOx127U3csWn6eXuJBIScmVsAKTnA3YGOlcb4Z+PGoeN/iRp2o+DPgnd3Mc0sVpea7PAZJ47Xf82HRcKAGY4LkV9OecdzMP+ED/algkT93o/xCsSki/wAK6jbDIb0BZDj3Jr2evIf2trOaL4YweLrFS1/4T1a11eAr12pIFcfQq2T9K9Zs7qG+sre+t2DQXMSzRkd1YBh+hoAlpDS0UAIaKDQKAA0lLRQAlFFFABRRRQAUUUUAOptOptABS9qSlFAAKKMUCgApKWkoAKUUlKKACloooA8d/aNT+0/E3wr8Mk5jv/FkVzKv95LdC5B9ua7v4q+OdK+HXgq78W63Bdz2VtJGjx2qq0jGRwowGIHU569q4T4s/vf2jPg5bt90SarNj3W3XH86n/a38JeJvG/wcn8P+E9OOoahLfwSNCJUj/dpuJOXIHXbxmgDrrT4i+FrnxEnh4XU8eqNoq62bd4G+W1IzksPl3D+7mrnw58aaD4/8LQ+JfDc082nTSPGjTQmNtyHDcH3r5FMH7R1h4z1LxVd/CsXF7eeHv7BxbpuSKHaAHULIfm4+ntX0R+yd4e1Pwv8B9B0jWtPuNP1BHuJJ7edCsiFp3IyD04wfxoA9UrjbZRrXjSSR/mgtiSB2wvA/M8119w/l28sn91C35CvPPDninwr4ekuP+Eh8SaPpNxOFMaXt7HCzqM5IDEZGa+Tz6P1rMMHgn8Lk5vz5Fdfiengn7OhVrLdJJfM9HHJ9zXgn7PmPFH7QnxV8dy/vEtb2LQ7JjztSLh8fXy0P416b/wtD4bL83/CwPC3HP8AyFof/iq8f/Yg8SeG18FX9vc6/pUeuaz4jurkWT3aC4lyEwQmdxyAe3avrDzD4o+I1xcD4heJAJ5QBq110c/89mr6w/YLkkf4O/EBnkZiJmwSc4/0Zq+SviP/AMlD8Sf9ha6/9HNX1l+wR/yRv4gf9d2/9JmoA+M/tNx/z3l/77NSI9867ka5ZfUFiKrV92fsF+LvDj/C5/ChndtWsri4vLlPsrlIoWK7WaTbsBPYZyfSlKSinKTskNJt2R5N+xx8PJ7/AFiT4j+IYpW0zSJNmmwzZxdXnUNg9Vj+8f8Aa2+hrp/2rfiXcaZpkvhLRpZn1bUV3X88YOYIW/hyP4n/AEX6ivZviP8AEzwZoOsWh8X62mk2k277PEsLyOUHU7UBIye54/KmxftL/AuKJYo/E5VFGFH9l3HA/wC+K+Jw1KXEGYLG1F/s9J+4v5pdZei6f8OevUksDQ9lH+JLfyXY/P7wv/aH/CTaVu+1AfbYc53f3xX62yf6xvqa8r8I/Hr4S+K/Ell4d0HX/tWp30nl28R0+ZN7YJxuZABwD1NepV9ueOeD/tXeJNI8FSeH9VsfAei+JfGesT/2dpkt/aibylUg4A6k7pAAAR9489q888TeP/2rvBegP4s8ReHtDtNCsGQ3NssUBCozBRkI5cDJAyDxmvUf2tPAGteMfDGh6z4a1GwsNZ8N6iL23e9nWGMg7f42+UMGRCN3BwRVX4n+Dviv8TvgT4d8PnVtK03W791bxAfNXyJ4QSRsMYbcMiNsLwfWgDvfEM1r8QfgVqF1BGRb694ckmjQnJXzICyj8CR+VVv2c9TbWPgR4MvpHLyf2VFC7HqTHmM/+gV0Pgvw5F4Y+H2k+FEnNzHpumpZeay48zam0tjtnk4rz/8AY4kL/s7eHVP/ACzlvIx9BdSgUAevUUUlAAaOaDRQAUUUUAFJRRQAUUUUAFFFFADqTFLSUAJS0lKKACikpaAA0dqKSgApaSigB1FIKWgDx74xg2/x4+DeonhDf6haE+8luMfyrs/i/Z+Or/wNc23w51K207xE00RhnuAuwJu+cHcrD7vt2rif2rC2meHvCHjBTtHhzxVZXczekLMY3/D5lr2Y4JypyOx9aAPkTxn4G+PekeHbjXvHHx+sdEtogdpS8ljV5MErGCqINxwcAZr179kbxnrfjn4KWGreIbl7vUre6ms5blx80wQgqx9ThgCe+K77x54P8O+OfD50HxRp4v8ATmmSYwmRky6fdOVIPc96u+GtB0bwzotvougabbabp1uCIreBNqrk5J9yTySeTQBJr93Dp+g6jf3Ebyw2tpLNIiHDMqoWIHuQK+NPEPx8+AniKeK48QfCXVdVmhTZHJcyxlkXOcDDjjOTX2hqdpHqGmXenynEd1A8DH0DqVP86/JPxboWoeGPE2peHtVhaG90+4e3mRhjlTjP0IwQe4IrGWHpSqxqyiuZaJ9VfctVJKLinoz7++FPw++B/wASfh9aeLdJ+GWnWMF6ZkSGfJkRkdk52tjqM/jXOfsPeBvBl34Cg8UXPh6yl8RadrVzCl8wPmx7du0DnHAYjpXzR8Gfj947+Fuky6Nov9n32lySmYWt9CziNzjJQqykZwMjJHtXVz/tZePodIudO0Dw/wCFPD/2gszS2FiysrsMFwC5Xd7kGtiDxv4jkH4h+JCCCDq11gj/AK7NX1n+wP8A8kb+IH/Xdv8A0mavjCWR5ZXlldnkdizMxyST1Jr7z/Yn8K3Wifs+6rfak0dm3iSeWS1Nw2xfL8ryo2JPZm3EeoxQwPjz4J+D5PHXxO0Tw79luLi0muVe+MI5jtlIMjE/wjbxn3Ffe1tBLa6U2keHNOtbeMIVtLCBRDCWAOxTgdM9z9a8puLnwR+zb8OG06zdNT8Q6gn+kzr8st/IP4V7pbofz9ya878A/tZ+JvDWmT2994Y07Wbua6knN1LO0ZRWxiNQAcKuMDmviczwlbiOrGNCbjQg3d9JvqkuqWqvtd6XPXw9WOAi3ON5vZdv67DvGP7OHx78W+IbnXNbtdKnu7hsn/iZRhUXsijso7Csb/hkz4yf9AzSv/BlHXd/8Ns69/0IOlf+B0n+FH/DbOvf9CDpX/gdJ/hX2dOnClBQgrJaJI8mUnJ3e434Cfs4/FDwd8YPDnibW7DTo9OsLoyXDR3yOwXYw4UdeSK+16+K4v219feRU/4QLShuIH/H9J/hX2jA5kgjkIwXRWx6ZGasR81/twXFjd6l8N/C2vai+neHdS1h5NUnD7VWNDGuSfYSOcnpnNeH/EBLDxXH4/8AiDbeMruw0/wxcWuk+EoorjAuljxGFQ5B4jQSfLz8xJr7d+JnhLwT4y0RNM8b6daX1pG/mRCVyjxtjGUZSGBx6da4y1+Cnwh1vwzZeHbfw3KukaTetdxxC5kUTTOoDNId25+FUcnpwK5XjcOqyw7mud9L6/caKlNwc7adzr/AOo6g/wAG9D1fWpmlvz4fhubqV+rP5AZmPuetcn+yDbNbfs6+Ft4wZluJ/wAHuJGH863vj3q8Phj4G+LL+LZAsOkSW8AXgK0i+UgH4sK0vhForeHfhV4V0N12yWek28cg/wBvywW/8eJrqMzqaKKKAENFFFABRQaSgAooooAKKKKACiiigB1NpaSgANL2pKUUAIetLQaSgBc0GikoAKKKKAClFIKdQByXxk8Mf8Jl8LPEnhpVDTXthILfPaZRvj/8fVaqfAPxR/wmPwf8N627ZujZrb3YPVZ4v3cgI7HK5/Gu3yQQR1FeK/C5v+EA+O3ir4dT/utK8RE+IdBz93e3FzCvuCNwA7L70Ae2UUUUAFeA/tR+HfhTqfh228YeOfDuqPb/AGg2cmt6NtFxbgEqjSA8PGWBAJDY4x1r3DxFf/2T4e1PVcZ+xWc1xj/cQt/SuK+FH9j+Pf2fvD8OpRRajYapoyQXsbHIZ9u2UH0YOG56gjNAHzp4T/ZU8A+O/D8PiPwV8Tr+40qdmVGl05WdWU4KsNykMPQgdQe9UvFX7LfgfwlqejWHiT4rXdlLrVz9lsP+JISkkuQNpcSFUPzD72KseHNM+JX7NfxefR9E0PUvF3hLXpCbe3tY2ZpwOhGAdk6A4ORhh7Yxd+OPxAGo20C/GGbTrSK1uFu7LwXoUyzX3mgEK13eciAcnKphjnoKAO00X9l74QfD60l8S+NNWutUtbEebK+pSrDarj+8i8t/uknPTBrwL9qD4wp8Vry203w3aDT/AAnoD7YN7iN7hmwgfy8jAAXCqASoJJxnA6rwLo/jr9qXxC9z4g1qLRvBeizKhsLWbJjyMhUQkszkZzLJnvjPSu2/au+D/wAN/BPwSfUfDPha2sr6O/tYRdeZI8hUsQ2SzHrjmgDJf9nj4e+LrtLy4+PcWr3rxIm4zW8j4CgBR+8zgdMVJ4j/AGRPBHh3w5eeItY+JOo2ul2URmnuDYIyqo9MMSTyAAOTmvaL79nP4MajbKJfA9rAzIPntrmaIjj2fH6V8+/Ez4Q6Vc/Few+Dvwu8Ra/EtxAbnxBDc3zT2VjEuGTcgxlhwcEnlk9aUYqKSSshttu7Nzw3+yB4O8Q6BY67pXxB1eawvoVntpG0xYy6N0baxBGevIrnviV+zt8JfhytkfGHxY1HTmvS32eMaX5ruFxk7UJIHIGTxmu71z4v/Er4DfYfD/xJ0nQPEmnNAY9Nu9KuVt5yqLhQ8WOF6DOwD0JNcX8KPC2vfF3x2/xn+KMW7SUkzpWnuCEumQ/IiKekCHkn+I8c5ascTiaWFpSrVpWjHVsqnTlUkoRV2zotG/Y48Lajp1nqlp481k29zEk8PmaasbFWAKkqzAqcY4IzX1pEohgRC3EaBcn0A61xJ8Zah/zwtfyP+NVtS8TX9/atakRRq/3vLByw9OtfHVuP8qjTbp8zl0VrXfqerDJMS5JSsl6kevyQ6lrjf2bCzbztGCT5jeoHaun8DQPBpU3mIyOZ2BVhgjAAo8I6L/Z8Iu7lR9qkHAP/ACzX0+vrW+Bk1lw1w9WhiP7VxT5ak7vlSskpfr/T1KzDHQdP6tS1ira+h4v+00W8Q3/gb4YwHc/iPXI57xRziztv3kpPtnH5V7OcZ4GB2HpXivwlf/hYHxt8V/E45k0fSF/4R3QGP3XCHdcTL9WOAfRsdq9qr708UKKKSgANJmlNJQAtBoooASiiigAooooAKKKKAF7UlLSUAFLSUvSgBDSiiigApKWigBKKKKAAUtJSigANeY/tDeEdU17wzZeJPCw2+LPC1z/aWklRzLt/1sB9Q6jGO5AHevTqOhyOtAHO/DLxjpfj7wRp3inSWxDdx/vYSfmt5Rw8Te6tke4we9dJXg/ieOb4G/EW48aWMEj/AA98S3C/2/bRKT/ZV4xwLtVH8DHhh/8AYivdLW4gu7WK6tZo57eZBJFLGwZXUjIYEdQR3oAj1Ozg1HTbrT7kEwXUDwSgf3XUqf0NfC9jZ/tF/ADVL/QPDWm3+raDJcM9u0dgb21lB6OoUExsRjI459etfeFKCR0JFAHxKf8Ahrf4rL9imW/8O6XMMSO0a6bFt9zgSsPYZrK8W/ssfEfwS1h4m8MXOm+L7m1ZZ7i1+zAsJAcnEUuRMv6n+7X3caKAPzmuvjV4k8MfE+LxnaeGB4a8TlRBr1gEeO01JRjl4WG6N+OoJ5AIwc59G+Pv7Qngf4nfA5tIskvtN11r62mexuIiygIx3FZF+UgZ74PtX174l8M+HPE1t9n8RaDpmrRYwFvLVJcfQsMj8K891D9nL4LXspkfwPawsTk+RczRj8g+BQB5b8Xv2u/D1hor6b8N4ptT1SSPYNQuYDHBbnGNyo3zOw7ZAH16V5D8Jfif44tdPvdG+FXhG71Txdrcnnaxr9xGbq5lkJJwoxsjQEk5ctkkk44x9c6R+z/8G9LlElv4C02V16G6aScfk7EfpXomladp2k2a2elafaWFsv3YbaFYkH4KAKAPmH4U/swahqWvf8Jn8bNWk1vU5WEp037QZQW6jz5P4gP7i8e5HFfUkVrawwRW8NtDHDCgSKNYwFRRwFA6AD0FSZpc1MoqSs0CdiPyIP8AnjF/3wKUQwg5EMYP+4KfRUexh/KiuZ9wryv9orxbqWm6HZeB/Cjb/F/i2Q2Onqp5t4jxNcN6Kq559eexrtPiH4w0TwJ4SvPE3iC48qztl+VF5eaQ/djQd2Y8D8+gNcF8DfCWt3ms3/xZ8fQeX4o1yMJZWTcjSbHqkIz0cjBbv+JatSTvvh74V03wR4K0rwrpK4tdPgEQfGDK/V5D7sxJP1reoooAKQ0ZpKAClpKKAFNApKWgANJRRQAUUUUAFFFFAC9qSlPSkoAKKKKACgUUUABooooAKKKKACiiigB1FIDRQBBqVlZ6lp9xp2oWsV1Z3MbRTwSruSRGGCpHcGvCbK61b9nrVRp2ptd6r8KryfFle8yTaBIx/wBVJ3aAk8Ht9eD79UN7a217ZzWd7bxXNtOhjmhlQMkingqwPBB9KAFsLu1v7KC+sbmG6tbhBJDNC4ZJFPIZSOCKmNeG3Pgrxr8Ir2bVvhUj6/4UlkMt54RuZjvgzyz2ch6euw/+PcY7z4Z/FDwh8QYXj0W+aDVIOLvSb1fJvLZh1DRnk4PcZFAHa0UUUAFFFFABRRRQAUUUAE9KACsDx94x8PeBfDU/iDxLfpZ2cXCjrJM/aONerMfQfU4HNcb49+MmlaXrB8KeC9Pm8aeL3yq6bpzbo7c/3riUfLGo7859cdaq+BvhXqd94kh8efFnUoPEHiaP5rGwiH/Ev0kdcRIeGcf3z3Hc80AZvgbwp4h+Jni20+JfxLsHsNNs28zwz4Zl5FsD0ubgd5TwQD049AK9tJyaCSTk0UAFIaKQ0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAKelJSnpSUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAKKWm0uaAFrhfiR8KfBvjuVL7VLGWy1mHm31jTpDb3kJHQiRfvY9GzXc0tAHi62nx68BfLZXOmfE/RU+7HduLLU0X03/ckOO5yTVi1/aF8HWc62XjfSfEfge+ztMer6c4iJ/2ZEBBHvxXsFR3MEF1A1vdQRXELcNHKgdT9QeKAOd0H4g+BNeQNo3jLQL3PRY7+Pd/3yTkflXQxXNtKu6K4hkHqkgI/SuJ1v4O/CrWZGk1D4f+H3kb7zxWohY/jHtNc9L+zd8GXbK+Eni9otSuUH5CSgD1S4vrG2Utc31rAB1Mkyr/ADNcj4j+Lfwy8PK39reOtBhdRzHHdrNJ/wB8R7m/Sudtf2cvgzA4c+DI7gj/AJ+L64kH6vXW+Hvhr8PPDzrJovgjw/ZSL0kSxQv/AN9EE/rQBwjfHSXxAxg+GPw88T+LZD927kg+w2I9zLJ2/AVG/gD4qePzn4k+NI/D+jv97QfDBKGRf7sty3zH0IGRXtQ4UKOFHQDoKKAMDwN4N8L+CNHGleFdFtdLtuN/lLl5T6u5+Zz7kmt+ikoAKM0hooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAFNJSmkoAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAClzSUUAOopMmjmgBaKSigBaKSigBaSgmkoAUmkoooAKKKKACiiigAooooAKKKKACiiigAooooAKKMUUAFFFHSgD/9k="

def get_logo_html(width=180, align="center"):
    margin = "margin-left: auto; margin-right: auto;" if align == "center" else "margin: 0;"
    return f"""
    <div style="text-align: {align}; padding: 5px;">
        <img src="data:image/jpeg;base64,{LOGO_B64}" width="{width}px" style="display: block; {margin} max-width: 100%; height: auto; border-radius: 6px;" alt="JE Global Logistics Logo" />
    </div>
    """

# Initialize Global Session State
if 'db_init' not in st.session_state:
    st.session_state.db_init = True
    st.session_state.current_user = None
    
    # User Database (Unlimited Admins and Brokers)
    st.session_state.users = [
        {'id': 'admin', 'name': 'Admin (Owner)', 'email': 'admin@jegloballogistics.com', 'password': 'admin2026!', 'role': 'admin'},
        {'id': 'b1', 'name': 'John Doe (Broker 1)', 'email': 'jdoe@jegloballogistics.com', 'password': 'broker123', 'role': 'broker'},
        {'id': 'b2', 'name': 'Sarah Smith (Broker 2)', 'email': 'ssmith@jegloballogistics.com', 'password': 'broker123', 'role': 'broker'},
        {'id': 'b3', 'name': 'Mike Johnson (Broker 3)', 'email': 'mjohnson@jegloballogistics.com', 'password': 'broker123', 'role': 'broker'},
        {'id': 'b4', 'name': 'Alex Rivera (Broker 4)', 'email': 'arivera@jegloballogistics.com', 'password': 'broker123', 'role': 'broker'},
        {'id': 'b5', 'name': 'Emily Davis (Broker 5)', 'email': 'edavis@jegloballogistics.com', 'password': 'broker123', 'role': 'broker'},
        {'id': 'b6', 'name': 'Carlos Gomez (Broker 6)', 'email': 'cgomez@jegloballogistics.com', 'password': 'broker123', 'role': 'broker'},
    ]
    
    # Client CRM Database
    st.session_state.clients = [
        {'id': 'C101', 'name': 'Caterpillar Midwest', 'contact': 'David Miller', 'phone': '(312) 555-0199', 'email': 'dmiller@cat.com', 'address': 'Peoria, IL', 'broker_id': 'admin', 'type': 'Repeated'},
        {'id': 'C102', 'name': 'Apex Auto Haulers', 'contact': 'Robert Chen', 'phone': '(404) 555-0143', 'email': 'logistics@apex.com', 'address': 'Atlanta, GA', 'broker_id': 'b1', 'type': 'Repeated'},
        {'id': 'C103', 'name': 'Titan Steel & General Freight', 'contact': 'Amanda Ross', 'phone': '(713) 555-0188', 'email': 'aross@titan.com', 'address': 'Houston, TX', 'broker_id': 'b2', 'type': 'New'},
    ]
    
    # Carrier Database
    st.session_state.carriers = [
        {'mc': 'MC-987654', 'name': 'Eagle Express Logistics', 'phone': '(800) 555-8822', 'email': 'dispatch@eagle.com', 'w9': True, 'coi': True, 'auth': True, 'driver': 'James Wilson - (800) 555-8823', 'safer': True, 'motus': True, 'scam_call': True, 'status': 'Approved'},
        {'mc': 'MC-456123', 'name': 'Reliable Freight Lines', 'phone': '(888) 555-3344', 'email': 'pete@reliable.com', 'w9': True, 'coi': False, 'auth': True, 'driver': 'Pending', 'safer': True, 'motus': False, 'scam_call': False, 'status': 'Pending Admin Review'},
    ]
    
    # Loads Database
    st.session_state.loads = [
        {
            'id': 'JE-2026-1001', 'broker_id': 'admin', 'customer': 'Caterpillar Midwest', 'type': 'Repeated',
            'phone': '(312) 555-0199', 'email': 'dmiller@cat.com', 'billing': 'Peoria, IL', 'pickup': 'Peoria, IL', 'delivery': 'Tampa, FL',
            'client_total': 4500.0, 'driver_pay': 3600.0, 'broker_fee': 900.0, 'commodity': 'Heavy Equipment CAT D6',
            'year': '2022', 'make': 'CAT', 'model': 'D6T', 'dims': 'L:22ft W:8.5ft H:10ft', 'weight': '42000 lbs', 'trailer': 'Lowboy / RGN',
            'mc': 'MC-987654', 'carrier': 'Eagle Express', 'dispatch': 'Mark Stevens', 'driver_phone': '(800) 555-8823',
            'car_email': 'dispatch@eagle.com', 'c_pay_meth': 'QuickPay', 'p_date': '2026-10-18', 'd_date': '2026-10-21',
            'status': 'Signed & Confirmed', 'signed_by': 'Mark Stevens (Eagle Express)', 'signed_date': '2026-10-16 10:15 AM'
        },
        {
            'id': 'JE-2026-1002', 'broker_id': 'b1', 'customer': 'Apex Auto Haulers', 'type': 'Repeated',
            'phone': '(404) 555-0143', 'email': 'logistics@apex.com', 'billing': 'Atlanta, GA', 'pickup': 'Atlanta, GA', 'delivery': 'Dallas, TX',
            'client_total': 2800.0, 'driver_pay': 2200.0, 'broker_fee': 600.0, 'commodity': 'Automobiles (3 Sedans)',
            'year': '2024', 'make': 'Toyota', 'model': 'Camry', 'dims': '45ft Enclosed', 'weight': '11500 lbs', 'trailer': 'Car Hauler / Enclosed',
            'mc': 'MC-456123', 'carrier': 'Reliable Freight', 'dispatch': 'Pete Taylor', 'driver_phone': '(888) 555-3344',
            'car_email': 'pete@reliable.com', 'c_pay_meth': 'Check on Delivery', 'p_date': '2026-10-20', 'd_date': '2026-10-22',
            'status': 'Awaiting Carrier Signature', 'signed_by': None, 'signed_date': None
        },
    ]

# -----------------------------------------------------------------------------
# LOGIN SCREEN (SHOWS FIRST IF NOT LOGGED IN)
# -----------------------------------------------------------------------------
if st.session_state.current_user is None:
    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_mid, c_right = st.columns([1, 2, 1])
    with c_mid:
        st.markdown(get_logo_html(220, align="center"), unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>JE Global Logistics LLC</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #475569;'>TMS Portal - Secure Login</h4>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("login_form", clear_on_submit=False):
            login_email = st.text_input("Corporate Email (@jegloballogistics.com)").strip()
            login_pass = st.text_input("Password", type="password").strip()
            submit_login = st.form_submit_button("🔑 Login to TMS Portal", use_container_width=True)
            
            if submit_login:
                user_match = next(
                    (u for u in st.session_state.users if u['email'].lower() == login_email.lower() and u['password'] == login_pass),
                    None
                )
                if user_match:
                    st.session_state.current_user = user_match
                    st.success(f"Welcome, {user_match['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please try again.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Default Admin Credentials for testing:**\n- **Email:** `admin@jegloballogistics.com`\n- **Password:** `admin2026!`")
    
    st.stop()  # Stop execution here until user logs in

# -----------------------------------------------------------------------------
# MAIN APPLICATION (WHEN LOGGED IN)
# -----------------------------------------------------------------------------
curr_u = st.session_state.current_user

# Sidebar Configuration
st.sidebar.markdown(get_logo_html(160, align="center"), unsafe_allow_html=True)
st.sidebar.markdown(f"### 👤 {curr_u['name']}")
st.sidebar.write(f"**Email:** {curr_u['email']}")
st.sidebar.write(f"**Role:** `{curr_u['role'].upper()}`")

if curr_u['role'] == 'admin':
    admin_mode = st.sidebar.radio("Admin Operating View", ["Company Overview (All Brokers)", "My Active Book (Owner Broker)"])
else:
    admin_mode = "Broker Mode"

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.current_user = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("JE Global Logistics LLC\n7901 4th St N STE 300\nSt. Petersburg FL 33702\n*We dont pay detention, delays or tonu.*")

# Main Header
h_col1, h_col2 = st.columns([1, 4])
with h_col1:
    st.markdown(get_logo_html(130, align="left"), unsafe_allow_html=True)
with h_col2:
    st.title("JE Global Logistics LLC - TMS Portal")
    st.caption("Transportation Management System (Cars, General Freight, LTL, Heavy Equipment)")

# Define Navigation Tabs
tab_list = ["📊 Dashboard", "📦 Load Dispatch", "👥 Customers (CRM)", "🛡️ Carriers & Documents", "📝 RateCon & Signature Hub"]
if curr_u['role'] == 'admin':
    tab_list.append("⚙️ User Management")

tabs = st.tabs(tab_list)

# -----------------------------------------------------------------------------
# TAB 1: DASHBOARD
# -----------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Brokerage Financial Dashboard")
    loads_v = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    
    rev = sum(l['client_total'] for l in loads_v)
    dpay = sum(l['driver_pay'] for l in loads_v)
    profit = sum(l['broker_fee'] for l in loads_v)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Client Revenue", f"${rev:,.2f}")
    c2.metric("Total Driver / Carrier Pay", f"${dpay:,.2f}")
    c3.metric("Broker Net Profit", f"${profit:,.2f}")
    st.markdown("---")
    
    st.markdown("### Recent Active Loads")
    if loads_v:
        df_dash = pd.DataFrame(loads_v)[['id', 'customer', 'commodity', 'trailer', 'client_total', 'driver_pay', 'broker_fee', 'status']]
        st.dataframe(df_dash, use_container_width=True)
    else:
        st.info("No active loads found for this view.")

# -----------------------------------------------------------------------------
# TAB 2: LOAD DISPATCH
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Dispatch & Order Entry (All Freight Types)")
    with st.expander("➕ Create New Load Order", expanded=False):
        with st.form("new_load_form"):
            st.markdown("#### 1. Customer Information")
            col1, col2, col3 = st.columns(3)
            ctype = col1.selectbox("Customer Status", ["Repeated Customer", "New Customer"])
            cname = col2.text_input("Customer Name*")
            cphone = col3.text_input("Customer Phone*")
            cemail = st.text_input("Customer Email*")
            cbill = st.text_input("Billing Address*")
            
            st.markdown("#### 2. Route & Contacts")
            p_addr = st.text_input("Pick-Up Address*")
            d_addr = st.text_input("Delivery Address*")
            
            st.markdown("#### 3. Financial Breakdown")
            f1, f2 = st.columns(2)
            ctot = f1.number_input("Client Total ($)*", min_value=0.0, step=100.0)
            dpay_in = f2.number_input("Driver / Carrier Pay ($)*", min_value=0.0, step=100.0)
            st.info(f"Calculated Broker Fee: **${ctot - dpay_in:,.2f}**")
            
            st.markdown("#### 4. Freight Specs (Cars, General Freight, LTL, Heavy Equipment)")
            s1, s2 = st.columns(2)
            comm = s1.text_input("Commodity Description*")
            trailer = s2.selectbox("Trailer Type*", ["Dry Van", "Reefer", "Car Hauler / Enclosed", "Car Hauler / Open", "Flatbed", "Stepdeck", "Lowboy / RGN", "LTL / Partial", "Hotshot"])
            weight = st.text_input("Weight (lbs)*")
            
            st.markdown("#### 5. Carrier Information")
            cmc = st.text_input("Carrier MC# / DOT#*")
            car_name = st.text_input("Carrier Name*")
            car_email = st.text_input("Carrier Email (for Ratecon)*")
            disp_contact = st.text_input("Dispatch Contact Name*")
            drv_phone = st.text_input("Driver Phone Number")
            p_date = st.date_input("Pick Up Date", datetime.date.today())
            d_date = st.date_input("Delivery Date", datetime.date.today() + datetime.timedelta(days=3))
            
            submit_load = st.form_submit_button("Save Load Order & Prepare Ratecon")
            if submit_load:
                new_id = f"JE-2026-{len(st.session_state.loads)+1001}"
                st.session_state.loads.append({
                    'id': new_id, 'broker_id': curr_u['id'], 'customer': cname, 'type': ctype, 'phone': cphone, 'email': cemail, 'billing': cbill, 'pickup': p_addr, 'delivery': d_addr,
                    'client_total': float(ctot), 'driver_pay': float(dpay_in), 'broker_fee': float(ctot - dpay_in), 'commodity': comm, 'year': '', 'make': '', 'model': '', 'dims': '', 'weight': weight, 'trailer': trailer,
                    'mc': cmc, 'carrier': car_name, 'dispatch': disp_contact, 'driver_phone': drv_phone, 'car_email': car_email, 'c_pay_meth': 'QuickPay', 'p_date': str(p_date), 'd_date': str(d_date),
                    'status': 'Awaiting Carrier Signature', 'signed_by': None, 'signed_date': None
                })
                st.success(f"Load {new_id} Created Successfully!")
                st.rerun()

    st.markdown("### Active Orders List")
    l_disp = st.session_state.loads if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [l for l in st.session_state.loads if l['broker_id'] == curr_u['id']]
    for ld in l_disp:
        st.write(f"📦 **{ld['id']}** | {ld['customer']} | {ld['commodity']} ({ld['trailer']}) | Carrier Pay: **${ld['driver_pay']:,.2f}** | Broker Fee: **${ld['broker_fee']:,.2f}** | Status: `{ld['status']}`")

# -----------------------------------------------------------------------------
# TAB 3: CUSTOMERS
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Customers Directory (Isolated by Broker)")
    cust_v = st.session_state.clients if (curr_u['role'] == 'admin' and admin_mode == 'Company Overview (All Brokers)') else [c for c in st.session_state.clients if c['broker_id'] == curr_u['id']]
    st.dataframe(pd.DataFrame(cust_v), use_container_width=True)
    
    with st.expander("➕ Register New Customer", expanded=False):
        with st.form("new_cust_form"):
            nc_name = st.text_input("Company / Customer Name*")
            nc_contact = st.text_input("Primary Contact Person*")
            nc_phone = st.text_input("Phone Number*")
            nc_email = st.text_input("Email Address*")
            nc_address = st.text_input("Address / Location*")
            sub_c = st.form_submit_button("Add Customer")
            if sub_c:
                new_c_id = f"C{100 + len(st.session_state.clients) + 1}"
                st.session_state.clients.append({
                    'id': new_c_id, 'name': nc_name, 'contact': nc_contact, 'phone': nc_phone, 'email': nc_email, 'address': nc_address, 'broker_id': curr_u['id'], 'type': 'New'
                })
                st.success(f"Customer {nc_name} added successfully!")
                st.rerun()

# -----------------------------------------------------------------------------
# TAB 4: CARRIERS & DOCUMENTS
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Carrier Directory & Document Vault")
    st.caption("Required Certificate Holder: JE Global Logistics LLC | 7901 4th St N STE 300 St. Petersburg FL 33702")
    
    with st.expander("📥 Upload Carrier Compliance Documents (W9, COI, Authority)", expanded=False):
        with st.form("doc_upload_form"):
            mc_in = st.text_input("MC# / DOT#*")
            car_in = st.text_input("Carrier Name*")
            ph_in = st.text_input("Phone*")
            em_in = st.text_input("Email*")
            w9_f = st.file_uploader("Upload W9 Form", type=['pdf', 'png', 'jpg'])
            coi_f = st.file_uploader("Upload COI", type=['pdf', 'png', 'jpg'])
            auth_f = st.file_uploader("Upload Authority Certificate", type=['pdf', 'png', 'jpg'])
            drv_in = st.text_input("Driver First/Last Name & Phone Number*")
            sub_doc = st.form_submit_button("Upload Documents to Database")
            if sub_doc:
                st.session_state.carriers.append({
                    'mc': mc_in, 'name': car_in, 'phone': ph_in, 'email': em_in, 'w9': w9_f is not None, 'coi': coi_f is not None, 'auth': auth_f is not None, 'driver': drv_in, 'safer': False, 'motus': False, 'scam_call': False, 'status': 'Pending Admin Review'
                })
                st.success("Documents uploaded successfully!")
                st.rerun()
                
    st.markdown("### Carrier Directory & Verification Queue")
    for car in st.session_state.carriers:
        with st.expander(f"🚛 {car['name']} ({car['mc']}) - Status: {car['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Phone:** {car['phone']} | **Email:** {car['email']}")
                st.write(f"**Driver Info:** {car['driver']}")
                st.write(f"- W9: {'✅ Uploaded' if car['w9'] else '❌ Missing'}")
                st.write(f"- COI (Certificate Holder Verified): {'✅ Uploaded' if car['coi'] else '❌ Missing'}")
                st.write(f"- Authority Cert: {'✅ Uploaded' if car['auth'] else '❌ Missing'}")
            with col2:
                if curr_u['role'] == 'admin':
                    st.write("**Admin Verification Controls:**")
                    s_chk = st.checkbox("SAFER Active Status Verified", value=car['safer'], key=f"s_{car['mc']}")
                    m_chk = st.checkbox("Motus Safety Rating Verified", value=car['motus'], key=f"m_{car['mc']}")
                    c_chk = st.checkbox("Anti-Scam Phone Call Check (Official SAFER Number)", value=car['scam_call'], key=f"c_{car['mc']}")
                    if st.button(f"Approve Carrier {car['mc']}", key=f"btn_{car['mc']}"):
                        car['safer'] = s_chk
                        car['motus'] = m_chk
                        car['scam_call'] = c_chk
                        car['status'] = "Approved"
                        st.success("Carrier Approved!")
                        st.rerun()

# -----------------------------------------------------------------------------
# TAB 5: RATECON & E-SIGNATURE HUB
# -----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Rate Confirmation & E-Signature Hub")
    if st.session_state.loads:
        sel_id = st.selectbox("Select Order to View Ratecon", [l['id'] for l in st.session_state.loads])
        ld_t = next(l for l in st.session_state.loads if l['id'] == sel_id)
        
        # Generated RateCon Preview Card with Embedded Logo
        d_pay_formatted = f"{ld_t['driver_pay']:,.2f}"
        
        ratecon_html = f"""
        <div style="border: 2px solid #0f172a; border-radius: 10px; padding: 20px; background-color: #ffffff; color: #0f172a;">
            <div style="text-align: center; margin-bottom: 15px;">
                <img src="data:image/jpeg;base64,{LOGO_B64}" width="180px" style="display: inline-block; max-width: 100%; height: auto;" />
                <h2 style="margin: 5px 0 0 0; color: #0f172a;">JE GLOBAL LOGISTICS LLC</h2>
                <p style="margin: 0; font-size: 13px; color: #475569;">7901 4th St N STE 300, St. Petersburg, FL 33702 | Phone: (800) 555-0199</p>
                <h3 style="margin: 10px 0 0 0; color: #2563eb;">OFFICIAL RATE CONFIRMATION</h3>
            </div>
            <hr style="border: 1px solid #cbd5e1;">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                <div>
                    <p><b>Order ID:</b> {ld_t['id']}</p>
                    <p><b>Pick-Up Date:</b> {ld_t['p_date']}</p>
                    <p><b>Delivery Date:</b> {ld_t['d_date']}</p>
                </div>
                <div>
                    <p><b>Carrier:</b> {ld_t['carrier']} ({ld_t['mc']})</p>
                    <p><b>Dispatch Contact:</b> {ld_t['dispatch']}</p>
                    <p><b>Driver Phone:</b> {ld_t['driver_phone']}</p>
                </div>
            </div>
            <hr style="border: 1px solid #cbd5e1;">
            <p><b>Route:</b> {ld_t['pickup']} ➔ {ld_t['delivery']}</p>
            <p><b>Commodity & Equipment:</b> {ld_t['commodity']} ({ld_t['trailer']}) | Weight: {ld_t['weight']}</p>
            <div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 10px; margin: 15px 0;">
                <h3 style="margin: 0; color: #1e3a8a;">AGREED CARRIER PAY: ${d_pay_formatted} USD</h3>
            </div>
            <p style="color: #dc2626; font-weight: bold; text-align: center; font-size: 14px; margin: 15px 0;">
                *** SPECIAL TERMS & CONDITIONS: We dont pay detention, delays or tonu. ***
            </p>
            <hr style="border: 1px solid #cbd5e1;">
            <p><b>E-Signature Status:</b> <span style="font-weight: bold; color: #2563eb;">{ld_t['status']}</span></p>
        </div>
        """
        st.markdown(ratecon_html, unsafe_allow_html=True)
        
        if ld_t['signed_date']:
            st.success(f"✅ Signed By: {ld_t['signed_by']} on {ld_t['signed_date']}")
        else:
            st.warning("⏳ Awaiting E-Signature from Carrier...")
            
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("📧 Send Ratecon to Carrier Email"):
                ld_t['status'] = 'Awaiting Carrier Signature'
                st.success(f"Ratecon emailed to {ld_t['car_email']}!")
        with col_s2:
            signer = st.text_input("Carrier Representative Signature Name", value=ld_t['dispatch'])
            if st.button("✍️ Simulate E-Sign Confirmation"):
                ld_t['status'] = 'Signed & Confirmed'
                ld_t['signed_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                ld_t['signed_by'] = f"{signer} ({ld_t['carrier']})"
                st.balloons()
                st.success("✅ Ratecon E-Signed and confirmed!")
                st.rerun()
    else:
        st.info("No load orders registered yet.")

# -----------------------------------------------------------------------------
# TAB 6: USER MANAGEMENT (ADMIN ONLY)
# -----------------------------------------------------------------------------
if curr_u['role'] == 'admin':
    with tabs[5]:
        st.subheader("⚙️ User Management Console (Admin Only)")
        st.caption("Unlimited Brokers & Admins - Create, Edit Passwords, or Delete Any User")
        
        col_u1, col_u2 = st.columns(2)
        
        # ADD NEW USER FORM
        with col_u1:
            st.markdown("### ➕ Add New User")
            with st.form("add_user_form", clear_on_submit=True):
                u_name = st.text_input("Full Name*")
                u_email = st.text_input("Corporate Email (@jegloballogistics.com)*").strip()
                u_pass = st.text_input("Password*", type="password").strip()
                u_role = st.selectbox("Role*", ["broker", "admin"])
                submit_u = st.form_submit_button("Add User to System")
                
                if submit_u:
                    if not u_name or not u_email or not u_pass:
                        st.error("Please fill in all required fields (*).")
                    elif any(u['email'].lower() == u_email.lower() for u in st.session_state.users):
                        st.error("A user with this email address already exists.")
                    else:
                        new_u_id = f"user_{len(st.session_state.users)+1}"
                        st.session_state.users.append({
                            'id': new_u_id,
                            'name': u_name,
                            'email': u_email,
                            'password': u_pass,
                            'role': u_role
                        })
                        st.success(f"User '{u_name}' ({u_role.upper()}) added successfully!")
                        st.rerun()

        # DELETE OR RESET USER FORM
        with col_u2:
            st.markdown("### 🔑 Reset User Password")
            with st.form("reset_pass_form"):
                user_reset_email = st.selectbox("Select User", [u['email'] for u in st.session_state.users], key="reset_sel")
                new_pass_in = st.text_input("New Password", type="password")
                submit_reset = st.form_submit_button("Update Password")
                if submit_reset:
                    target_u = next((u for u in st.session_state.users if u['email'] == user_reset_email), None)
                    if target_u and new_pass_in:
                        target_u['password'] = new_pass_in
                        st.success(f"Password for {target_u['name']} updated successfully!")
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### ❌ Delete User")
            st.write("You can remove any broker or admin account from the system.")
            
            # Select user to delete
            del_email = st.selectbox("Select User to Remove", [u['email'] for u in st.session_state.users], key="delete_sel")
            target_del = next((u for u in st.session_state.users if u['email'] == del_email), None)
            
            if target_del:
                st.warning(f"Are you sure you want to delete **{target_del['name']}** (`{target_del['email']}`)?")
                if st.button(f"🗑️ Permanently Delete {target_del['name']}", type="primary", key="btn_del_user"):
                    st.session_state.users = [u for u in st.session_state.users if u['email'] != del_email]
                    st.success(f"User '{target_del['name']}' has been removed from the system.")
                    
                    # If admin deleted their own current account
                    if curr_u['email'].lower() == del_email.lower():
                        st.session_state.current_user = None
                    
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📋 All Registered Users")
        users_df = pd.DataFrame(st.session_state.users)[['id', 'name', 'email', 'role', 'password']]
        st.dataframe(users_df, use_container_width=True)
