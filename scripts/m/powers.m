function Q = powers(chcnt,data, srate)
    nchan=chcnt;
    
    Q = table(); 
    for ichan = 1:nchan
        fprintf('Channel %d \n', ichan)
        % Using example Matlab code showing how to compute power spectrum of epoched data
        [spectra,freqs] = spectopo(data(ichan,:,:), 0, srate);
    
        % Set the following frequency bands: delta=1-4, theta=4-8, alpha=8-13, beta=13-30, gamma=30-80.
        deltaIdx = freqs>1 & freqs<4;
        thetaIdx = freqs>4 & freqs<8;
        alphaIdx = freqs>8 & freqs<13;
        betaIdx  = freqs>13 & freqs<30;
        gammaIdx = freqs>30 & freqs<80;
    
        % Compute absolute power.
        tempTable = table(); 
    
        tempTable.channel = ichan;
        tempTable.deltaPower = mean(10.^(spectra(deltaIdx)/10));
        tempTable.thetaPower = mean(10.^(spectra(thetaIdx)/10));
        tempTable.alphaPower = mean(10.^(spectra(alphaIdx)/10));
        tempTable.betaPower  = mean(10.^(spectra(betaIdx)/10));
        tempTable.gammaPower = mean(10.^(spectra(gammaIdx)/10));
        Q = [Q;tempTable];
    end
end
