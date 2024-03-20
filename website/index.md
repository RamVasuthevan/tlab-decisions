---
layout: default
---

TLAB decisions

<table>
  <thead>
    <tr>
      <th>Year</th>
      <th>Bookmark Name</th>
      <th>File Name</th>
    </tr>
  </thead>
  <tbody>
    {% for decision in site.data.decisions %}
      <tr>
        <td>{{ decision.year }}</td>
        <td>{{ decision.bookmark_name }}</td>
        <!-- Update the link to point to the correct file location -->
        <td><a href="{{ site.baseurl }}/assets/tlab-decisions/2017/{{ decision.file_name }}">{{ decision.file_name }}</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>