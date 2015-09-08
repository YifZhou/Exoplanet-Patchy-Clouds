#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
from scipy.io import readsav
from squareMean import squareMean
"""comment
"""


def JHratio1(jlc, hlc, jerr, herr):
    jarg = np.argsort(jlc)
    harg = np.argsort(hlc)
    jlc = jlc[jarg]
    jerr = jerr[jarg]  # relative uncertainty
    hlc = hlc[harg]
    herr = herr[harg]  # relative uncertainty
    Jmin = jlc[0:5].mean()  # mean value of maximum 5
    Jmin_err = (jerr[0:5]**2).mean()**0.5
    Jmax = jlc[-5:].mean()  # mean value of maximum 5
    Jmax_err = (jerr[-5:]**2).mean()**0.5

    Hmin = hlc[0:5].mean()  # mean value of maximum 5
    Hmin_err = herr[0:5].mean()
    Hmax = hlc[-5:].mean()  # mean value of maximum 5
    Hmax_err = herr[-5:].mean()

    JHratio = ((Jmax - Jmin) / jlc.mean()) / ((Hmax - Hmin) / hlc.mean())
    Jerr = np.sqrt(Jmax_err**2 + Jmin_err**2) / (Jmax - Jmin)
    Herr = np.sqrt(Hmax_err**2 + Hmin_err**2) / (Hmax - Hmin)
    JHratio_err = np.sqrt(Jerr**2 + Herr**2)

    return JHratio, JHratio_err


if __name__ == '__main__':
    M2139 = readsav('2MASSJ2139_spec_bin.sav')
    jh2139 = JHratio1(M2139['jlc'], M2139['hlc'],
                      M2139['jlcerr'], M2139['hlcerr'])
    S0136 = readsav('SIMP0136_spec_bin.sav')
    jh0136 = JHratio1(S0136['jlc'], S0136['hlc'],
                      S0136['jlcerr'], S0136['hlcerr'])

    M1821 = readsav('2m1821spectralratio.sav')
    min1821spec = M1821.minspec5est[M1821.xxx]
    max1821spec = M1821.maxspec5est[M1821.xxx]
    wl1821 = M1821.westher[M1821.xxx]
    snr1821 = M1821.snr1821
    min125 = min1821spec[(wl1821 > 1.1423) & (wl1821 < 1.3908)].sum()
    min125_err = np.sqrt(
        ((min1821spec[(wl1821 > 1.1423) & (wl1821 < 1.3908)] /
          snr1821[(wl1821 > 1.1423) & (wl1821 < 1.3908)])**2).sum())
    max125 = max1821spec[(wl1821 > 1.1423) & (wl1821 < 1.3908)].sum()
    max125_err = np.sqrt(
        ((max1821spec[(wl1821 > 1.1423) & (wl1821 < 1.3908)] /
          snr1821[(wl1821 > 1.1423) & (wl1821 < 1.3908)])**2).sum())
    min160 = min1821spec[(wl1821 > 1.4028) & (wl1821 < 1.6710)].sum()
    min160_err = np.sqrt(
        ((min1821spec[(wl1821 > 1.4028) & (wl1821 < 1.6710)] /
          snr1821[(wl1821 > 1.4028) & (wl1821 < 1.6710)])**2).sum())
    max160 = max1821spec[(wl1821 > 1.4028) & (wl1821 < 1.6710)].sum()
    max160_err = np.sqrt(
        ((max1821spec[(wl1821 > 1.4028) & (wl1821 < 1.6710)] /
          snr1821[(wl1821 > 1.4028) & (wl1821 < 1.6710)])**2).sum())

    jh1821 = ((max125 - min125) / (max125 + min125)) /\
        ((max160 - min160) / (max160 + min160))
    Jerr = np.sqrt(max125_err**2 + min125_err**2) / (max125 - min125)
    Herr = np.sqrt(max160_err**2 + min160_err**2) / (max125 - min125)
    JH1821_err = np.sqrt(Jerr**2 + Herr**2)
    print('2M2139    {0:.2f}  {1:.2f}%'.format(
        jh2139[0], 100 * jh2139[1]))
    print('S0136     {0:.2f}  {1:.2f}%'.format(
        jh0136[0], jh0136[1] * 100))
    print('2M1821    {0:.2f}  {1:.2f}%'.format(
        jh1821, JH1821_err * 100))
