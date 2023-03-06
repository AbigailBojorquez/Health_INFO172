<template>
  <div id="app">
    <l-map :center="[37.0902, -95.7129]" :zoom="4" style="height: 500px;" :options="mapOptions">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-choropleth-layer :data="usCountyData" titleKey="county" idKey="county" :value="value" :extraValues="extraValues" geojsonIdKey="NAME" :geojson="usCountyGeojson" :colorScale="colorScale">
        <template slot-scope="props">
          <div class="info-control-wrapper">
            <l-info-control :item="props.currentItem" :unit="props.unit" title="County" placeholder="Hover over a county"/>
          </div>
          <l-reference-chart title="US State Populations" :colorScale="colorScale" :min="props.min" :max="props.max" position="topright"/>
        </template>
      </l-choropleth-layer>
    </l-map>
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
      colorScale: ["e7d090", "e9ae7b", "de7062"],
      value: {
        key: "low_risk",
        metric: " # of Estimated Cases of Cold/Flu"
      },
      extraValues: [
        {
          key: "high_risk",
          metric: " # of Estimated Cases of Pneumonia/Bronchitis"
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
  margin-left: 100px;
  margin-right: 100px;
}

#map {
  background-color: rgb(0, 0, 0);
}
</style>
