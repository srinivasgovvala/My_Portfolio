// Ambient music system
(function() {
  const musicToggleNav = document.getElementById('musicToggleNav');
  const musicPlayer = document.getElementById('music-player');
  const playBtn = document.getElementById('musicPlayBtn');
  const prevBtn = document.getElementById('musicPrevBtn');
  const nextBtn = document.getElementById('musicNextBtn');
  const volumeSlider = document.getElementById('musicVolume');
  const trackNameEl = document.getElementById('musicTrackName');

  let audio = null;
  let tracks = [];
  let currentIndex = 0;
  let currentSection = 'home';
  let isPlaying = false;
  let userEnabled = false;

  async function loadTracks(section) {
    try {
      const res = await fetch(`/music/tracks/?section=${section}`);
      const data = await res.json();
      tracks = data.tracks || [];
      currentIndex = 0;
    } catch (_) {}
  }

  function initAudio() {
    if (!audio) {
      audio = new Audio();
      audio.loop = false;
      audio.addEventListener('ended', nextTrack);
      audio.addEventListener('error', nextTrack);
    }
  }

  function playTrack(index) {
    if (!tracks.length || !audio) return;
    currentIndex = ((index % tracks.length) + tracks.length) % tracks.length;
    const track = tracks[currentIndex];
    if (!track || !track.url) return;
    audio.src = track.url;
    audio.volume = parseFloat(volumeSlider ? volumeSlider.value : 0.4);
    audio.play().then(() => {
      isPlaying = true;
      if (playBtn) playBtn.textContent = '❚❚';
      if (trackNameEl) trackNameEl.textContent = track.title + (track.artist ? ' · ' + track.artist : '');
      if (musicToggleNav) musicToggleNav.classList.add('playing');
    }).catch(() => {});
  }

  function pauseTrack() {
    if (audio) { audio.pause(); isPlaying = false; }
    if (playBtn) playBtn.textContent = '▶';
    if (musicToggleNav) musicToggleNav.classList.remove('playing');
  }

  function nextTrack() {
    if (tracks.length > 1) {
      playTrack(currentIndex + 1);
    } else if (tracks.length === 1) {
      playTrack(0);
    }
  }
  function prevTrack() {
    if (tracks.length > 1) {
      playTrack(currentIndex - 1);
    } else if (tracks.length === 1) {
      playTrack(0);
    }
  }

  async function enableMusic(section) {
    userEnabled = true;
    initAudio();
    await loadTracks(section);
    if (tracks.length) {
      playTrack(0);
      if (musicPlayer) musicPlayer.hidden = false;
      if (musicToggleNav) musicToggleNav.title = 'Music on — click to stop';
    }
  }

  function disableMusic() {
    userEnabled = false;
    pauseTrack();
    if (musicPlayer) musicPlayer.hidden = true;
    if (musicToggleNav) { musicToggleNav.classList.remove('playing'); musicToggleNav.title = 'Toggle ambient music'; }
  }

  // Toggle on nav button
  if (musicToggleNav) {
    musicToggleNav.addEventListener('click', () => {
      if (!userEnabled) {
        enableMusic(currentSection).then(() => {
          if (!tracks.length) {
            musicToggleNav.title = 'No music tracks added yet';
            setTimeout(() => { musicToggleNav.title = 'Toggle ambient music'; }, 3000);
          }
        });
      } else if (isPlaying) {
        disableMusic();
      } else {
        if (tracks.length) { initAudio(); playTrack(currentIndex); }
        else enableMusic(currentSection);
      }
    });
  }

  if (playBtn) playBtn.addEventListener('click', () => { isPlaying ? pauseTrack() : playTrack(currentIndex); });
  if (prevBtn) prevBtn.addEventListener('click', prevTrack);
  if (nextBtn) nextBtn.addEventListener('click', nextTrack);
  if (volumeSlider) volumeSlider.addEventListener('input', () => { if (audio) audio.volume = parseFloat(volumeSlider.value); });

  // Section-based track switching
  function detectSection() {
    const sections = [
      { id: 'contact', key: 'contact' },
      { id: 'future', key: 'future' },
      { id: 'projects', key: 'projects' },
    ];
    let found = 'home';
    const y = window.scrollY + window.innerHeight / 2;
    sections.forEach(({ id, key }) => {
      const el = document.getElementById(id);
      if (el && el.offsetTop <= y) found = key;
    });
    return found;
  }

  window.addEventListener('scroll', () => {
    if (!userEnabled) return;
    const newSection = detectSection();
    if (newSection !== currentSection) {
      currentSection = newSection;
      loadTracks(newSection).then(() => { if (tracks.length && isPlaying) playTrack(0); });
    }
  }, { passive: true });
})();
