const WMO = {
  0:  ['☀️',  'Céu limpo'],
  1:  ['🌤️', 'Principalmente limpo'],
  2:  ['⛅',  'Parcialmente nublado'],
  3:  ['☁️',  'Nublado'],
  45: ['🌫️', 'Nevoeiro'],
  48: ['🌫️', 'Nevoeiro com geada'],
  51: ['🌦️', 'Garoa leve'],
  53: ['🌦️', 'Garoa'],
  55: ['🌦️', 'Garoa intensa'],
  61: ['🌧️', 'Chuva leve'],
  63: ['🌧️', 'Chuva'],
  65: ['🌧️', 'Chuva forte'],
  71: ['❄️',  'Neve leve'],
  73: ['❄️',  'Neve'],
  75: ['❄️',  'Neve forte'],
  80: ['🌧️', 'Pancadas leves'],
  81: ['🌧️', 'Pancadas'],
  82: ['🌧️', 'Pancadas fortes'],
  95: ['⛈️',  'Trovoada'],
  96: ['⛈️',  'Trovoada com granizo'],
  99: ['⛈️',  'Trovoada com granizo forte'],
};

function wmo(code) {
  return WMO[code] || ['🌡️', 'Desconhecido'];
}

const DAYS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];

async function loadWeather(lat, lon) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}` +
    `&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,wind_speed_10m` +
    `&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max` +
    `&timezone=auto&forecast_days=4`;

  const res = await fetch(url);
  const d = await res.json();
  const c = d.current;
  const daily = d.daily;

  const [icon, desc] = wmo(c.weather_code);

  // reverse geocode for city name
  let city = '';
  try {
    const geo = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`);
    const gd = await geo.json();
    city = gd.address.city || gd.address.town || gd.address.village || gd.address.county || '';
  } catch (_) {}

  if (city) {
    document.getElementById('weather-location').textContent = `— ${city}`;
  }

  // skip today (index 0) in forecast, show next 3 days
  const forecastHtml = [1, 2, 3].map(i => {
    const date = new Date(daily.time[i] + 'T12:00:00');
    const dayName = DAYS[date.getDay()];
    const [fi] = wmo(daily.weather_code[i]);
    const rain = daily.precipitation_probability_max[i];
    return `
      <div class="weather-day">
        <div class="weather-day-name">${dayName}</div>
        <div class="weather-day-icon">${fi}</div>
        <div class="weather-day-range">${Math.round(daily.temperature_2m_max[i])}° / ${Math.round(daily.temperature_2m_min[i])}°</div>
        ${rain != null ? `<div class="weather-day-rain">💧 ${rain}%</div>` : ''}
      </div>`;
  }).join('');

  document.getElementById('weather-content').innerHTML = `
    <div class="weather-current">
      <div class="weather-icon">${icon}</div>
      <div>
        <div class="weather-temp">${Math.round(c.temperature_2m)}°C</div>
        <div class="weather-feels">Sensação ${Math.round(c.apparent_temperature)}°C · ${desc}</div>
      </div>
    </div>
    <div class="weather-meta">
      <span>💧 ${c.relative_humidity_2m}%</span>
      <span>🌬️ ${Math.round(c.wind_speed_10m)} km/h</span>
      ${c.precipitation > 0 ? `<span>🌧️ ${c.precipitation} mm</span>` : ''}
    </div>
    <div class="weather-forecast">${forecastHtml}</div>`;
}

function init() {
  const content = document.getElementById('weather-content');
  if (!content) return;

  if (!navigator.geolocation) {
    content.innerHTML = '<p class="weather-loading">Geolocalização não suportada.</p>';
    return;
  }

  navigator.geolocation.getCurrentPosition(
    pos => loadWeather(pos.coords.latitude, pos.coords.longitude).catch(() => {
      content.innerHTML = '<p class="weather-loading">Erro ao carregar clima.</p>';
    }),
    () => {
      content.innerHTML = '<p class="weather-loading">Permissão de localização negada.</p>';
    }
  );
}

init();
