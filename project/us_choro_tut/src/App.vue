<template>
  <div>
    <div id="map-selectors">
      <input type="radio" id="map1" value="map1" v-model="selectedMap" name="map-selectors">
      <label for="map1">Low Risk</label>
      <input type="radio" id="map2" value="map2" v-model="selectedMap" name="map-selectors">
      <label for="map2">High Risk</label>
    </div>
    <div v-if="selectedMap === 'map1'" id="app">
      <l-map :center="[37.0902, -95.7129]" :zoom="4" style="height: 700px;" :options="mapOptions">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-choropleth-layer :data="usCountyData" titleKey="county" idKey="county" :value="lowRiskValue" :extraValues="lowRiskExtraValues" geojsonIdKey="NAME" :geojson="usCountyGeojson" :colorScale="colorScale">
          <template slot-scope="props">
            <div class="info-control-wrapper">
              <l-info-control :item="props.currentItem" :unit="props.unit" title="County" placeholder="Hover over a county"/>
            </div>
            <l-reference-chart title="Estimated Cases by Tweets" :colorScale="colorScale" :min="props.min" :max="props.max" position="topright"/>
          </template>
        </l-choropleth-layer>
      </l-map>
    </div>
    <div>
      <div v-if="selectedMap === 'map2'" id="app">
        <l-map :center="[37.0902, -95.7129]" :zoom="4" style="height: 700px;" :options="mapOptions">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-choropleth-layer :data="usCountyData" titleKey="county" idKey="county" :value="highRiskValue" :extraValues="highRiskExtraValues" geojsonIdKey="NAME" :geojson="usCountyGeojson" :colorScale="colorScale">
            <template slot-scope="props">
              <div class="info-control-wrapper">
                <l-info-control :item="props.currentItem" :unit="props.unit" title="County" placeholder="Hover over a county"/>
              </div>
              <l-reference-chart title="Estimated Cases by Tweets" :colorScale="colorScale" :min="props.min" :max="props.max" position="topright"/>
            </template>
          </l-choropleth-layer>
        </l-map>
      </div>
    </div>
  </div>
</template>

<script>
import { InfoControl, ReferenceChart, ChoroplethLayer } from 'vue-choropleth'

//import { geojson } from './data/py-departments-geojson'
import usCountyGeojson from './data/us_counties.json'
import { usCountyData } from './data/low_high_counts_county'
import {LMap, LTileLayer} from 'vue2-leaflet';

export default {
  name: "app",
  components: { 
    LMap,
    LTileLayer,
    'l-info-control': InfoControl, 
    'l-reference-chart': ReferenceChart, 
    'l-choropleth-layer': ChoroplethLayer 
  },
  data() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      usCountyData,
      usCountyGeojson,
      selectedMap: 'map1',
      colorScale: ["e7d090", "e9ae7b", "de7062"],
      lowRiskValue: {
        key: "low_risk",
        metric: " Estimated Cases of Cold/Flu"
      },
      lowRiskExtraValues: [
        {
          key: "high_risk",
          metric: " Estimated Cases of Pneumonia/Bronchitis"
        }
      ],
      highRiskValue: {
        key: "high_risk",
        metric: " Estimated Cases of Pneumonia/Bronchitis"
      },
      highRiskExtraValues: [
        {
          key: "low_risk",
          metric: " Estimated Cases of Cold/Flu"
        }
      ],
      mapOptions: {
        attributionControl: false
      },
      currentStrokeColor: '3d3213'
    }
  },
}
</script>
<style>
@import "../node_modules/leaflet/dist/leaflet.css";
body {
  background-color: #e7d090;
  margin-left: 0px;
  margin-right: 0px;
}

#map {
  background-color: rgb(0, 0, 0);
}

#map-selectors {
        display: inline-block;
        cursor: pointer;
        border-radius: 50%;
        border: 2px solid #ccc;
        width: 20px;
        height: 20px;
        content: center;
}

</style>
